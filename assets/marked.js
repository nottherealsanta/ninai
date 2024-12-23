import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

document.querySelectorAll('.vertex-container').forEach(div => {
    init_vertex_div(div);
});


function init_vertex_div(div, setFocus = false) {
    const vertex = div.querySelector('.vertex');
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


    div.addEventListener('click', (event) => {
        vertex.style.display = 'block';
        markdown.style.display = 'none';
        vertex.focus();
        event.stopPropagation();
    });
    if (isInputActive) {
        vertex.style.display = 'block';
        markdown.style.display = 'none';
        vertex.focus();
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