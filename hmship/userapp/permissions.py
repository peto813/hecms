from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user



class isQuerySetOwner(BasePermission): 

    def has_permission(self, request, view):
        

        for item in view.queryset:
            pass
            #print item.user.id == request.user.id
            #print item.values()
        if request.method in SAFE_METHODS:
            return True
        return False


class IsOwner(BasePermission): 

    # def has_permission(self, request, view):
    #     print request, 'peo'
    #     return False

    def has_object_permission(self, request, view, obj):
        model = obj.__class__.__name__ 
        if model == 'User':
            return  obj.id == request.user.id
        elif model == 'Logistics':
            return  obj.service.user.id == request.user.id
        elif model == 'Maintenance':
            return  obj.service.user.id == request.user.id
        elif model == 'Inspections':
            return  obj.service.user.id == request.user.id
        elif model == 'Auction_Products':
            return  obj.user.id == request.user.id
        elif model == 'Services':
            return  obj.user.id == request.user.id  
        elif model == 'Payments':
            return  obj.user.id == request.user.id
        elif model == 'Inspection_Reports':
            return  obj.inspection.service.user.id == request.user.id   
        return obj.user == request.user




# Create permission class.
class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False

class IsStaffOrReadOnly(BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff   
    def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		return request.user.is_staff
        # ip_addr = request.META['REMOTE_ADDR']
        # blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
        # return not blacklisted