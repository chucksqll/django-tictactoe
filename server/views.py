from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    return render(request, 'server/index.html')


class RoomView(TemplateView):
	template_name = 'server/room.html'
	board = [
		['','',''],
		['','',''],
		['','',''],
	]
	last_turn = 'o'


	def get_context_data(self, **kwargs):
		return super().get_context_data(
			board=self.board,
			**kwargs)
			

