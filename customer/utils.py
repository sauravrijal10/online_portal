def branch_check(user, customer_instance):
    print(f"User branch: {user.branch}")
    print(f"Customer branch: {customer_instance.branch}")
    return user.branch == customer_instance.branch if hasattr(user, 'branch') else False
