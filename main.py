from fasthtml.common import *
import sqlite3
import logging

app, rt = fast_app(
    live=True,
    pico=False,
    hdrs=(Link(rel="stylesheet", href="assets/main.css", type="text/css"),),
)

# configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def create_db(overwrite=False):
    # check if database exists
    if not os.path.exists("db.sqlite") or overwrite:
        # create a new database
        conn = sqlite3.connect("db.sqlite")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                        id TEXT PRIMARY KEY,
                        parent_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        content TEXT,
                        FOREIGN KEY (parent_id) REFERENCES nodes(id)
        """
        )
        # create index for parent_id
        conn.execute("CREATE INDEX IF NOT EXISTS parent_id_idx ON nodes (parent_id)")
        conn.commit()
        log.info("Database created")
    else:
        log.info("Database already exists")


create_db()


@rt("/")
def get():
    return Title("Ninai"), Main(
        H1("Ninai"),
        P("Welcome to Ninai!"),
        Input(
            type="text",
            value="Sample text",
            cls="vertex",
            hx_trigger="blur",
            hx_post="/change",
            hx_include="#gM2ks1l",
            id="gM2ks1l",
        ),
        Input(
            type="text",
            value="More Sample Text",
            cls="vertex",
            hx_trigger="blur",
            hx_get="/change",
            id="3u2nDj4",
        ),
    )


@rt("/change", methods=["POST"])
async def get(request):
    x = await request.form()
    print(x)
    print(type(x))
    return None
