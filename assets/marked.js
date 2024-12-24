import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

document.querySelectorAll('.vertex-container').forEach(div => {
    init_vertex_div(div);
});


function init_vertex_div(div, setFocus = false) {
    const vertex = div.querySelector('.vertex-edit');
    const markdown = div.querySelector('.markdown');
    let isInputActive = setFocus;

    const updateMarkdown = () => {
        const rawText = vertex.innerText;
        markdown.innerHTML = marked.parse(rawText,);
    };
    updateMarkdown();

    vertex.addEventListener('focus', () => {
        isInputActive = true;
    });


    vertex.addEventListener('blur', (event) => {
        console.log('Blur event fired', event);
        isInputActive = false;
        updateMarkdown()
        setTimeout(() => {
            vertex.style.display = 'none';
            markdown.style.display = 'block';
        }, 50);
    });

    vertex.addEventListener('keypress', (event) => {
        if (event.keyCode == 13 && !event.shiftKey) {
            event.preventDefault();
        }
        else if (event.keyCode == 13 && event.shiftKey) {
            // event.preventDefault();
        }
    });


    div.addEventListener('click', (event) => {
        vertex.style.display = 'block';
        markdown.style.display = 'none';
        vertex.focus();

        console.log('Click event fired', event);

        moveCursorToClickPosition(vertex, event);

        event.stopPropagation();
    });
    if (isInputActive) {
        vertex.style.display = 'block';
        markdown.style.display = 'none';
        vertex.focus();
        moveCursorToEnd(vertex);
    }


    document.addEventListener('click', function (event) {
        if (!div.contains(event.target)) {
            if (isInputActive) {
                vertex.dispatchEvent(new Event('blur'));
            }
        }
    });
}

window.init_vertex_div = init_vertex_div


function moveCursorToClickPosition(element, event) {
    // Create a range object for the text node within the element.
    const range = document.createRange();
    range.selectNodeContents(element);

    let clickPosition = event.clientX;
    let startPosition = range.getBoundingClientRect().left;

    let textNode = element.firstChild
    if (!textNode) return

    // Iterate over text nodes, and get width of those nodes.
    let start = 0;
    let end = textNode.textContent.length;
    while (start < end) {
        const mid = Math.floor((start + end) / 2);
        const midRange = document.createRange()
        midRange.setStart(textNode, 0)
        midRange.setEnd(textNode, mid)
        const rect = midRange.getBoundingClientRect();

        if (rect.right < clickPosition) {
            start = mid + 1;
        } else {
            end = mid;
        }
    }

    // Set the caret to the calculated position
    const selection = window.getSelection();
    range.setStart(textNode, start)
    range.collapse(true)
    selection.removeAllRanges()
    selection.addRange(range);
}
function moveCursorToEnd(element) {
    // Create a range object for the text node within the element.
    const range = document.createRange();
    range.selectNodeContents(element);
    range.collapse(false);

    // Set the caret to the end of the element.
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
}