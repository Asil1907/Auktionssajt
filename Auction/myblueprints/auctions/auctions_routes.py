from flask import Blueprint, render_template, request, redirect, flash
from dbrepositories.auction_repository import AuctionRepository
from dbrepositories.bid_repository import BidRepository

auctions_bp = Blueprint("auctions", __name__)

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
    bids = BidRepository.get_top_two(id)
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

# -------- ADMIN --------

@auctions_bp.route("/admin/create", methods=["GET", "POST"])
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
def admin_delete(id):
    AuctionRepository.delete(id)
    return redirect("/")


