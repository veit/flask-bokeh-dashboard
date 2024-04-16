try:
    import asyncio
except ImportError:
    raise RuntimeError("This requries at least Python3.4/asyncio")

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from bokeh.themes import Theme
from flask import Flask, render_template, request
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    print("This script is intended to be run with gunicorn. e.g.")
    print()
    print("    pipenv run gunicorn -w 4 main:app")
    print()
    print("will start the app on four processes")
    import sys

    sys.exit()

app = Flask(__name__)


def modify_doc(doc):
    flask_args = doc.session_context.request.arguments
    unit_type = flask_args.get("unit_type")[0].decode("utf-8")

    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)
    plot = figure(
        x_axis_type="datetime",
        y_range=(0, 25),
        y_axis_label=f"Temperature ({unit_type})",
    )
    plot.line("time", "temperature", source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling("{0}D".format(new)).mean()
        source.data = ColumnDataSource(data=data).data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change("value", callback)

    doc.add_root(column(slider, plot))
    doc.theme = Theme(filename="theme.yaml")


bkapp = Application(FunctionHandler(modify_doc))

# This is so that if this app is run using something like "gunicorn -w 4" then
# each process will listen on its own port
sockets, port = bind_sockets("127.0.0.1", 0)


@app.route("/", methods=["GET"])
def bkapp_page():
    dataset = request.args.get("dataset")

    if request.args.get("unit_type") is None:
        unit_type = "Celcius"
    else:
        unit_type = request.args.get("unit_type")

    script = server_document(
        "http://127.0.0.1:%d/bkapp" % port, arguments=dict(unit_type=unit_type)
    )

    return render_template(
        "index.html",
        script=script,
        app_name="Material Dashboard with Bokeh embedded in Flask",
        app_description="This Dashboard is served by a Bokeh server embedded in Flask.",
        app_icon="timeline",
        unit_type=unit_type,
        dataset=dataset,
    )


def bk_worker():
    asyncio.set_event_loop(asyncio.new_event_loop())

    bokeh_tornado = BokehTornado(
        {"/bkapp": bkapp}, extra_websocket_origins=["127.0.0.1:8000"]
    )
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()


from threading import Thread

Thread(target=bk_worker).start()
