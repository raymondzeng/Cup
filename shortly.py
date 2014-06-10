from cup import Cup

app = Cup()

@app.route('/')
def new_url(request):
    error = None
    url = ''
    if request.method == 'POST':
        url = request.form['url']
        short_id = url
        return redirect('/%s+' % short_id)
    return "HEllo"

@app.route('/<short_id>')
def follow_short_link(request, short_id):
    return "Damn"

@app.route('/<short_id>+')
def on_short_link_details(request, short_id):
    return "FOOO"

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, app)
