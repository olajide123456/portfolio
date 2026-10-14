from django.shortcuts import redirect

class CustomLoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')

        response = super().dispatch(request, *args, **kwargs)

        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response