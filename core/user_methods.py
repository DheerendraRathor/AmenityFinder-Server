"""
Contains core methods for the user which will be used project-wide
"""


def increase_plus_points(user, points):
    user.profile.plus_points += points
    user.profile.save()
    set_user_level(user)


def decrease_plus_points(user, points):
    user.profile.plus_points -= points
    user.profile.save()
    set_user_level(user)


def increase_minus_points(user, points):
    user.profile.minus_points += points
    user.profile.save()
    set_user_level(user)


def decrease_minus_points(user, points):
    user.profile.minus_points -= points
    user.profile.save()
    set_user_level(user)


def set_user_level(user):
    # TODO: Do something
    user.profile.save()
