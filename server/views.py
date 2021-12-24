from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    return render(request, 'server/index.html', {'room_names':list(RoomView.board.keys())})


class RoomView(TemplateView):
	template_name = 'server/room.html'
	board={}
	last_turn = {}


	def get_context_data(self, **kwargs):
		return super().get_context_data(
			**kwargs)
			

