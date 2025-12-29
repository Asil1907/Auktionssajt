from flask import Blueprint, render_template, request, redirect, flash
from dbrepositories.auction_repository import AuctionRepository
from dbrepositories.bid_repository import BidRepository

auctions_bp = Blueprint("auctions", __name__)

@auctions_bp.route("/")
def index():
    keyword = request.args.get("q")
    show_all = request.args.get("show_all")
    
    if keyword:
        auctions = AuctionRepository.search(keyword)
    elif show_all:
        auctions = AuctionRepository.get_all()
    else:
        auctions = AuctionRepository.get_active()

    return render_template(
        "auction_list.html",
        auctions=auctions,
        keyword=keyword,
        show_all=show_all
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
    if request.method == "POST":
        AuctionRepository.create(
            request.form["title"],
            request.form["description"],
            request.form["starting_bid"],
            request.form["end_datetime"]
        )
        return redirect("/")
    return render_template("admin_create.html")

@auctions_bp.route("/admin/delete/<int:id>")
def admin_delete(id):
    AuctionRepository.delete(id)
    return redirect("/")


