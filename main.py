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
        Script(
            src="assets/marked.js",
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


# async def add_sample_data():
#     id1 = await add_node("Idea 1")
#     id2 = await add_node("Idea 2", parent_id=id1, position=1)
#     id3 = await add_node("Idea 3", parent_id=id1, position=2)
#     id3a = await add_node("Idea 3a", parent_id=id3, position=1)
#     id3b = await add_node("Idea 3b", parent_id=id3, position=2)
#     id3c = await add_node("Idea 3c", parent_id=id3, position=3)

#     id4 = await add_node("Idea 4")
#     id5 = await add_node("Idea 5", parent_id=id4, position=1)
#     id5c = await add_node("Idea 5c", parent_id=id5, position=3)
#     id5a = await add_node("Idea 5a", parent_id=id5, position=1)
#     id5b = await add_node("Idea 5b", parent_id=id5, position=2)
#     id5d = await add_node("Idea 5d", parent_id=id5, position=4)
#     id6 = await add_node("Idea 6", parent_id=id4, position=2)


async def add_sample_data():
    # Core Ideas (no parent)
    id1 = await add_node("Project Alpha - Initial Brainstorm")
    id2 = await add_node("Personal Development Goals")
    id3 = await add_node("Research Topics for Next Quarter")

    # Project Alpha Details
    id1_1 = await add_node("Scope Definition", parent_id=id1, position=1)
    id1_2 = await add_node("Resource Allocation", parent_id=id1, position=2)
    id1_3 = await add_node("Timeline and Milestones", parent_id=id1, position=3)

    # Scope Definition Sub-points
    id1_1_1 = await add_node("Identify Core Features", parent_id=id1_1, position=1)
    id1_1_2 = await add_node("User Stories Workshop", parent_id=id1_1, position=2)
    id1_1_3 = await add_node("Market Analysis Review", parent_id=id1_1, position=3)

    # Resource Allocation Sub-points
    id1_2_1 = await add_node("Budget Planning", parent_id=id1_2, position=1)
    id1_2_2 = await add_node("Team Assignment", parent_id=id1_2, position=2)
    id1_2_3 = await add_node("Tooling and Software", parent_id=id1_2, position=3)

    # Timeline and Milestones Sub-points
    id1_3_1 = await add_node("Phase 1: Research", parent_id=id1_3, position=1)
    id1_3_2 = await add_node("Phase 2: Development", parent_id=id1_3, position=2)
    id1_3_3 = await add_node("Phase 3: Testing", parent_id=id1_3, position=3)
    id1_3_4 = await add_node("Phase 4: Launch", parent_id=id1_3, position=4)

    # Personal Development Goals
    id2_1 = await add_node("Skill Acquisition", parent_id=id2, position=1)
    id2_2 = await add_node("Networking", parent_id=id2, position=2)
    id2_3 = await add_node("Health and Wellbeing", parent_id=id2, position=3)

    # Skill Acquisition Sub-points
    id2_1_1 = await add_node("Learn Python", parent_id=id2_1, position=1)
    id2_1_2 = await add_node("Master SQL", parent_id=id2_1, position=2)
    id2_1_3 = await add_node("Public Speaking Course", parent_id=id2_1, position=3)

    # Networking Sub-points
    id2_2_1 = await add_node("Attend Industry Events", parent_id=id2_2, position=1)
    id2_2_2 = await add_node("Connect on LinkedIn", parent_id=id2_2, position=2)
    id2_2_3 = await add_node("Mentorship Program", parent_id=id2_2, position=3)

    # Health and Wellbeing Sub-points
    id2_3_1 = await add_node("Consistent Workout Schedule", parent_id=id2_3, position=1)
    id2_3_2 = await add_node("Mindfulness Practice", parent_id=id2_3, position=2)
    id2_3_3 = await add_node("Nutritional Diet Planning", parent_id=id2_3, position=3)

    # Research Topics for Next Quarter
    id3_1 = await add_node("## AI and Machine Learning", parent_id=id3, position=1)
    id3_2 = await add_node("Cybersecurity Trends", parent_id=id3, position=2)
    id3_3 = await add_node("Sustainable Technologies", parent_id=id3, position=3)

    # AI and Machine Learning Sub-points
    id3_1_1 = await add_node("Deep Learning Models", parent_id=id3_1, position=1)
    id3_1_2 = await add_node("Natural Language Processing", parent_id=id3_1, position=2)
    id3_1_3 = await add_node(
        "Computer Vision Applications", parent_id=id3_1, position=3
    )

    # Cybersecurity Trends Sub-points
    id3_2_1 = await add_node("Threat Landscape Analysis", parent_id=id3_2, position=1)
    id3_2_2 = await add_node("Emerging Security Protocols", parent_id=id3_2, position=2)
    id3_2_3 = await add_node("Data Privacy Regulations", parent_id=id3_2, position=3)

    # Sustainable Technologies Sub-points
    id3_3_1 = await add_node(
        "Renewable Energy Innovations", parent_id=id3_3, position=1
    )
    id3_3_2 = await add_node(
        "Resource Management Strategies", parent_id=id3_3, position=2
    )
    id3_3_3 = await add_node("Circular Economy Approaches", parent_id=id3_3, position=3)

    # Additional Random ideas
    id4 = await add_node("Organize Home Office", parent_id=None, position=1)
    id5 = await add_node("Plan a weekend trip", parent_id=None, position=2)
    id6 = await add_node("Read 'Sapiens' ", parent_id=None, position=3)
    id7 = await add_node("Try a new recipe", parent_id=id5, position=1)
    id8 = await add_node("Book a hotel", parent_id=id5, position=2)


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
    vals_str = (
        f"js:{{'id':'{id}','content': document.getElementById('{id}').innerText}}",
    )

    return Div(
        Div(
            Div(
                Div(
                    style="border-radius: 50%; height: 7px; width: 7px; background-color: light-dark(#f4f4f4, #666666);",
                ),
                cls="handle",
                style="",
            ),
            Div(
                Div(
                    content if content else "",
                    id=id,
                    contenteditable=True,
                    cls=f"vertex",
                    hx_trigger="blur",
                    hx_swap="none",
                    hx_post="update_vertex",
                    hx_vals=vals_str,
                    style="display: none;",
                ),
                Div(
                    cls="markdown",
                    style="display: block;",
                ),
                cls="vertex-container",
            ),
            style="display:flex;flex-direction:row; align-items:start;",
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

    source_tree = await get_children_recursive_cte(source[0])
    source_tree = source_tree[0]

    id = source_tree["id"]
    decendants = source_tree["children"]

    return Div(
        # vertex(source_tree, level=0),
        Div(
            source_tree["content"],
            style="margin: 10px 0",
        ),
        Div(
            *[vertex(d, level=1) for d in decendants],
            cls="sortable ",
            data_id=id,
        ),
        Hr(),
        id=id,
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


@rt("/update_vertex", methods=["POST"])
async def post(request):
    """ """
    request = (await request.form())._dict

    log.info(f"/update_vertex: {request}")

    id = request["id"]
    content = request["content"]

    await cursor.execute(
        "UPDATE nodes SET content = ? WHERE id = ?",
        (content, id),
    )
    await conn.commit()
    log.info("updated")

    return "ok"


@rt("/dnd", methods=["POST"])
async def post(request):
    """ """
    request = (await request.form())._dict
    id = request["id"]
    new_parent_id = request["new_parent_id"]
    new_prev_id = request["new_prev_id"]
    new_next_id = request["new_next_id"]

    # update parent_id
    await cursor.execute(
        "UPDATE nodes SET parent_id = ? WHERE id = ?",
        (new_parent_id, id),
    )
    await conn.commit()

    # get previous and next position

    async def get_position(id):
        fetchall = await (
            await cursor.execute("SELECT position FROM nodes WHERE id = ?", (id,))
        ).fetchall()
        if fetchall:
            return fetchall[0][0]
        else:
            return None

    new_prev_position = await get_position(new_prev_id)
    new_next_position = await get_position(new_next_id)

    # update position
    if new_prev_position and not new_next_position:
        new_postion = new_prev_position + 1
    elif new_next_position and not new_prev_position:
        new_postion = new_next_position / 2
    elif not new_prev_position and not new_next_position:
        new_postion = 1
    else:
        new_postion = (new_prev_position + new_next_position) / 2

    await cursor.execute(
        "UPDATE nodes SET position = ? WHERE id = ?",
        (new_postion, id),
    )
    await conn.commit()

    log.info(
        f" /dnd {id} {new_parent_id} {new_prev_position} {new_next_position} {new_postion}"
    )

    return "ok"
