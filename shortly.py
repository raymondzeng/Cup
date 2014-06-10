from cup import Cup
from werkzeug.wrappers import Request, Response

app = Cup()

def on_new_url(self, request):
    error = None
    url = ''
    if request.method == 'POST':
        url = request.form['url']
        short_id = url
        return redirect('/%s+' % short_id)
        
def on_follow_short_link(request, short_id):
    return Response("Damn");

def on_short_link_details(request, short_id):
    return Response("FOOO");

app.on_new_url = on_new_url
app.on_follow_short_link = on_follow_short_link
app.on_short_link_details = on_short_link_details

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, app)
