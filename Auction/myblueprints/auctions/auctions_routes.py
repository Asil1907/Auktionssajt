from flask import Blueprint, render_template, request, redirect, flash, session
from functools import wraps
from dbrepositories.auction_repository import AuctionRepository
from dbrepositories.bid_repository import BidRepository

auctions_bp = Blueprint("auctions", __name__)

# Decorator för att kräva inloggning
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Du måste logga in för att komma åt den här sidan.')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@auctions_bp.route("/")
def index():
    keyword = request.args.get("q")
    show_all = request.args.get("show_all")
    category = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    end_time = request.args.get("end_time")
    
    # Om sökord finns, sök
    if keyword:
        auctions = AuctionRepository.search(keyword)
    # Om filter finns, använd filter
    elif category or min_price or max_price or end_time:
        auctions = AuctionRepository.filter_auctions(
            category=category,
            min_price=int(min_price) if min_price else None,
            max_price=int(max_price) if max_price else None,
            end_time=int(end_time) if end_time else None,
            show_all=bool(show_all)
        )
    # Annars visa alla eller pågående
    elif show_all:
        auctions = AuctionRepository.get_all()
    else:
        auctions = AuctionRepository.get_active()
    
    # Hämta alla kategorier för filter-dropdown
    categories = AuctionRepository.get_all_categories()

    return render_template(
        "auction_list.html",
        auctions=auctions,
        keyword=keyword,
        show_all=show_all,
        categories=categories,
        selected_category=category,
        min_price=min_price,
        max_price=max_price,
        end_time=end_time
    )

@auctions_bp.route("/auction/<int:id>")
def detail(id):
    auction = AuctionRepository.get_by_id(id)
    bids = BidRepository.get_all_for_auction(id)
    bid_count = BidRepository.count_for_auction(id)
    highest_bid = BidRepository.get_highest(id)

    return render_template(
        "auction_detail.html",
        auction=auction,
        bids=bids,
        bid_count=bid_count,
        highest_bid=highest_bid
    )

@auctions_bp.route("/auction/<int:id>/bid", methods=["POST"])
def bid(id):
    bidder = request.form["bidder"]
    amount = request.form["amount"]
    BidRepository.create(id, bidder, amount)
    flash("Ditt bud är lagt!")
    return redirect(f"/auction/{id}")

@auctions_bp.route("/auction/<int:id>/like")
def like(id):
    AuctionRepository.like(id)
    return redirect(f"/auction/{id}")

@auctions_bp.route("/auction/<int:id>/dislike")
def dislike(id):
    AuctionRepository.dislike(id)
    return redirect(f"/auction/{id}")

@auctions_bp.route("/completed")
def completed():
    """Visa avslutade auktioner med bud"""
    auctions = AuctionRepository.get_completed_with_bids()
    return render_template("completed_auctions.html", auctions=auctions)

# -------- LOGIN/LOGOUT --------

@auctions_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Enkel autentisering (byt till databas i produktion)
        if username == "admin" and password == "admin123":
            session['logged_in'] = True
            session['username'] = username
            flash("Du är nu inloggad!")
            return redirect("/")
        else:
            flash("Fel användarnamn eller lösenord")
    
    return render_template("login.html")

@auctions_bp.route("/logout")
def logout():
    session.clear()
    flash("Du är nu utloggad")
    return redirect("/")

# -------- ADMIN --------

@auctions_bp.route("/admin/create", methods=["GET", "POST"])
@login_required
def admin_create():
    categories = ["Elektronik", "Fordon", "Hem & Trädgård", "Kläder & Accessoarer", "Sport & Fritid", "Samlarprylar", "Övrigt"]
    
    if request.method == "POST":
        AuctionRepository.create(
            request.form["title"],
            request.form["description"],
            request.form["starting_bid"],
            request.form["end_datetime"],
            request.form.get("category", "Övrigt")
        )
        flash("Auktion skapad!")
        return redirect("/")
    return render_template("admin_create.html", categories=categories)

@auctions_bp.route("/admin/delete/<int:id>")
@login_required
def admin_delete(id):
    AuctionRepository.delete(id)
    flash("Auktion borttagen!")
    return redirect("/")

@auctions_bp.route("/admin/edit/<int:id>", methods=["GET", "POST"])
@login_required
def admin_edit(id):
    categories = ["Elektronik", "Fordon", "Hem & Trädgård", "Kläder & Accessoarer", "Sport & Fritid", "Samlarprylar", "Övrigt"]
    
    if request.method == "POST":
        AuctionRepository.update(
            id,
            request.form["title"],
            request.form["description"],
            request.form["starting_bid"],
            request.form["end_datetime"],
            request.form.get("category", "Övrigt")
        )
        flash("Auktion uppdaterad!")
        return redirect(f"/auction/{id}")
    
    # GET - visa formulär med befintliga värden
    auction = AuctionRepository.get_by_id(id)
    return render_template("admin_edit.html", auction=auction, categories=categories)

@auctions_bp.route("/admin/bid/delete/<int:bid_id>/<int:auction_id>")
@login_required
def admin_delete_bid(bid_id, auction_id):
    BidRepository.delete(bid_id)
    flash("Bud borttaget!")
    return redirect(f"/auction/{auction_id}")
