import uuid
import asyncio
import aiosqlite
import logging
from fasthtml.common import *
from datetime import datetime
from rich import print, inspect

conn = None
cursor = None


async def startup():
    global conn, cursor
    conn = await aiosqlite.connect("db.sqlite")
    cursor = await conn.cursor()

    await create_db()


app, rt = fast_app(
    live=True,
    pico=False,
    hdrs=(
        Link(rel="stylesheet", href="assets/main.css", type="text/css"),
        NotStr(
            """<script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>"""
        ),
        Script(
            src="assets/sortable.js",
            type="module",
        ),
    ),
    on_startup=[startup],
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def create_id():
    return str(uuid.uuid4())


async def add_node(content, parent_id=None, position=0):
    id = create_id()
    await cursor.execute(
        "INSERT INTO nodes (id, parent_id, content, created_at, updated_at, position) VALUES (?, ?, ?, ?, ?, ?)",
        (id, parent_id, content, datetime.now(), datetime.now(), position),
    )
    await conn.commit()
    return id


async def add_sample_data():
    id1 = await add_node("Idea 1")
    id2 = await add_node("Idea 2", parent_id=id1, position=1)
    id3 = await add_node("Idea 3", parent_id=id1, position=2)
    id3a = await add_node("Idea 3a", parent_id=id3, position=1)
    id3b = await add_node("Idea 3b", parent_id=id3, position=2)
    id3c = await add_node("Idea 3c", parent_id=id3, position=3)

    id4 = await add_node("Idea 4")
    id5 = await add_node("Idea 5", parent_id=id4, position=1)
    id5c = await add_node("Idea 5c", parent_id=id5, position=3)
    id5a = await add_node("Idea 5a", parent_id=id5, position=1)
    id5b = await add_node("Idea 5b", parent_id=id5, position=2)
    id5d = await add_node("Idea 5d", parent_id=id5, position=4)
    id6 = await add_node("Idea 6", parent_id=id4, position=2)


async def create_db(overwrite=False):

    # check if db exists
    if overwrite:
        await conn.execute("DROP TABLE IF EXISTS nodes")
        await conn.commit()
        log.info("Database deleted")

    # check if table exists
    await cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='nodes'"
    )
    if await cursor.fetchall():
        log.info("Database already exists")
        return
    else:
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS nodes (
                        id TEXT PRIMARY KEY,
                        parent_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        content TEXT NOT NULL,
                        position REAL NOT NULL DEFAULT 0,
                        FOREIGN KEY (parent_id) REFERENCES nodes(id)
                    );
        """
        )
        # create index for parent_id
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS parent_id_idx ON nodes (parent_id)"
        )
        await conn.commit()
        log.info("Database created")

        await add_sample_data()


async def get_all_sources():
    await cursor.execute(
        "SELECT id, content, created_at, updated_at FROM nodes WHERE parent_id IS NULL ORDER BY updated_at DESC"
    )
    return await cursor.fetchall()


async def get_children_recursive_cte(parent_id):
    """
    Retrieves all children of a node recursively, ordered by position,
    using a single query with a CTE and converting the data to the required
    dictionary format.

    Args:
        parent_id: The ID of the parent node.

    Returns:
        A list of dictionaries, each representing a child node with
        'id', 'content', 'created_at', 'updated_at', 'position', and
        'children' (a list of its children), ordered by position.
    """
    await cursor.execute(
        """
        WITH RECURSIVE descendants(id, parent_id, content, created_at, updated_at, position, path) AS (
            SELECT id, parent_id, content, created_at, updated_at, position, CAST(id AS TEXT)
            FROM nodes
            WHERE id = ?
            UNION ALL
            SELECT n.id, n.parent_id, n.content, n.created_at, n.updated_at, n.position
            , CAST(d.path || '/' || n.id AS TEXT)
            FROM nodes n
            INNER JOIN descendants d ON n.parent_id = d.id
        )
        SELECT id, parent_id, content, created_at, updated_at, position, path
        FROM descendants
        ORDER BY position
    """,
        (parent_id,),
    )

    rows = await cursor.fetchall()
    nodes = {}
    for row in rows:
        id, parent_id, content, created_at, updated_at, position, path = row
        nodes[id] = {
            "id": id,
            "parent_id": parent_id,
            "content": content,
            "created_at": created_at,
            "updated_at": updated_at,
            "position": position,
            "children": [],
        }

    for id, node in nodes.items():
        if node["parent_id"] and node["parent_id"] in nodes:
            nodes[node["parent_id"]]["children"].append(node)

    return [n for n in nodes.values() if n["parent_id"] is None]


def vertex(node, level):

    id = node["id"]
    content = node["content"]
    vals_str = (f"js:{{'content': document.getElementById('{id}').innerText}}",)

    print(
        f"id: {id}, content: {content}, children: {node['children']}, vals_str: {vals_str}"
    )

    return Div(
        Div(
            Div(
                Div(
                    style="border-radius: 50%; height: 7px; width: 7px; background-color: light-dark(#f4f4f4, #666666);",
                ),
                cls="handle",
                style="height: 25px; width: 25px; border-radius: cursor: move;display:flex;align-items:center;justify-content:center;",
            ),
            Div(
                content if content else "",
                contenteditable=True,
                cls=f" vertex",
                hx_vals=vals_str,
            ),
            style="display:flex;flex-direction:row; align-items:center;",
        ),
        Div(
            *[vertex(d, level + 1) for d in node["children"]],
            cls="sortable",
            data_id=id,
        ),
        style=f"display:flex;flex-direction:column;",
        data_id=id,
    )


async def draw_source_vertex(source):

    print(f"source: {source}")
    source_tree = await get_children_recursive_cte(source[0])
    source_tree = source_tree[0]
    print(f"source_tree: {source_tree}")

    parent_id = source_tree["id"]
    decendants = source_tree["children"]

    return Div(
        # vertex(source_tree, level=0),
        source_tree["content"],
        Div(
            *[vertex(d, level=1) for d in decendants],
            cls="sortable",
            data_id=id,
        ),
        Hr(),
        id=parent_id,
        cls="source",
    )


@rt("/")
async def get():
    sources = await get_all_sources()

    return Title("Ninai"), Main(
        Div(
            *[await draw_source_vertex(source) for source in sources],
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


@rt("/dnd", methods=["POST"])
async def post(request):
    """ """
    x = await request.body()
    print(request, request.path_params, request.query_params, x)
    x = await request.form()
    print(x._dict)
    return "ok"
