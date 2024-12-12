from fasthtml.common import *
import sqlite3
import logging
from rich import print, inspect

app, rt = fast_app(
    live=True,
    pico=False,
    hdrs=(Link(rel="stylesheet", href="assets/main.css", type="text/css"),),
)

# configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()


def create_db(overwrite=False):

    # check if db exists
    if overwrite:
        conn.execute("DROP TABLE IF EXISTS nodes")
        conn.commit()
        log.info("Database deleted")

    # check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nodes'")
    if cursor.fetchall():
        log.info("Database already exists")
        return
    else:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS nodes (
                        id TEXT PRIMARY KEY,
                        parent_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        content TEXT,
                        FOREIGN KEY (parent_id) REFERENCES nodes(id)
                    );
        """
        )
        # create index for parent_id
        conn.execute("CREATE INDEX IF NOT EXISTS parent_id_idx ON nodes (parent_id)")
        conn.commit()
        log.info("Database created")


create_db()


def get_all_sources():
    cursor.execute("SELECT * FROM nodes WHERE parent_id IS NULL")
    return cursor.fetchall()


sources = get_all_sources()
log.info(sources)


def vertex(id, content=None):

    id = "sdf"
    vals_str = (f"js:{{'content': document.getElementById('{id}').innerText}}",)
    print(vals_str)

    return Div(
        content if content else "",
        id=id,
        contenteditable=True,
        hx_trigger="blur",
        hx_post="/change",
        hx_swap="none",
        cls="vertex",
        hx_vals=vals_str,
    )


@rt("/")
def get():
    return Title("Ninai"), Main(
        H1("Ninai"),
        P("Welcome to Ninai!"),
        Div(
            vertex("nwl32H3", "Idea 1"),
            style="display:flex;flex-direction:column",
        ),
    )


@rt("/change", methods=["POST"])
async def post(request):
    """ """
    x = await request.form()
    print(request, x)
    print(x._dict)
    return "ok"
