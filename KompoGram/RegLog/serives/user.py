def get_user_friend(user, friend_id):
    return user.friends.filter(id=friend_id).first()
