from twisted.web.server import Site


class RapuiSite(Site):

    def getResourceFor(self, request):
        """
        Get a resource for a request.

        This iterates through the resource hierarchy, calling
        getChildWithDefault on each resource it finds for a path element,
        stopping when it hits an element where isLeaf is true.
        """
        request.site = self
        # Sitepath is used to determine cookie names between distributed
        # servers and disconnected sites.
        request.sitepath = copy.copy(request.prepath)
        return resource.getChildForRequest(self.resource, request)


