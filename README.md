# RapUI
Synerty utility classes for serving a static site with twisted.web with user permissions.

Whats of interest?

* A conditional resource tree that is constructed upon each request

* Decorators for adding custom resource creators.

* Sub resource roots. Designed for placing file system roots in the resource tree,

# Conditional Resource Root
, with login
details from `twisted http session` as an argument. This means that resources for certain
users won't even exist, removing the need to permission checking on the render_GET/POST, etc.

Users who are not logged in will be served a static HTML page with embedded CSS/JS.
Unless a user is logged in, the server will not provide them with ANY resources, API 
or otherwise. (Though a public API would be a use case against this).

# Decorators

    from rapui.site.ResourceUtil import addResourceCreator
    
    @addResourceCreator

## Backstory
RapUI = Rapid UI, it's original purpose.

Backstory, RapUI used to have twisted template support, javascript, multi path search
etc, Synertys vortex, ng2-balloon-msg, and all the bower packages, which are availible
from npm.

All that has been stripped out into separate projects as we move to using angular-cli
and full client side template rendering (With hopes for Angular2 Universal in the future.)



