from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.receipts import ReceiptsShareRequest, Status, Receipts
from app.models.user import User
from app import db

friends = Blueprint('friends', __name__)

@friends.route('/friend-receipt')
@login_required
def display_receipts():
    """
    Display a list of all accepted receipt shares from friends
    """
    # Get all accepted receipt share requests where the current user is the receiver
    accepted_requests = (ReceiptsShareRequest
                        .query
                        .filter_by(receiver_id=current_user.uid, status=Status.ACCEPTED)
                        .all())
    
    # Create a list with sender information and receipt data
    friend_receipts = []
    
    for request in accepted_requests:
        # Get the sender's information
        sender = User.query.get(request.sender_id)
        
        # Get the receipt information
        receipt = Receipts.query.get(request.shared_receipt_id)
        
        if sender and receipt:
            friend_receipts.append({
                'request_id': request.request_id,
                'sender': sender,
                'receipt': receipt,
                'time_shared': request.time
            })
    
    return render_template('friend-receipt.html', 
                          friend_receipts=friend_receipts,
                          view_mode='list')

@friends.route('/friend-receipt/remove/<int:request_id>', methods=['POST'])
@login_required
def remove_shared_receipt(request_id):
    """
    Remove a shared receipt from your list (change status to REMOVED)
    """
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    
    # Check if the current user is the receiver
    if request.receiver_id != current_user.uid:
        abort(403)  # Forbidden
    
    # Change status to removed
    request.status = Status.REMOVED
    db.session.commit()
    
    flash('The shared receipt has been removed from your list.', 'success')
    return redirect(url_for('friends.display_receipts'))