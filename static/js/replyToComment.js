const replyBtn = document.querySelector("#reply-btn");
const comment_id = replyBtn.dataset.commentId;
const replyTextareaDiv = document.querySelector(`#reply-to-${comment_id}`);
replyBtn.addEventListener("click", () => {
    console.log(replyTextareaDiv);
    if (replyTextareaDiv.classList.contains("hidden")) {
        replyTextareaDiv.classList.remove("hidden");
    } else {
        replyTextareaDiv.classList.add("hidden");
    }
})

function replyToComment(comment_id) {
    const replyText = document.querySelector(`#textarea-${comment_id}`).value;

    fetch(`/reply-to-comment/${comment_id}`, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: replyText
        })
    })

    const repliesCount = document.querySelector("#replies-count");
    repliesCount.innerText = parseInt(repliesCount.innerText) + 1;
    const newReply = document.querySelector("#template-reply");
    newReply.children[1].children[1].innerText = replyText;
    const replies = document.querySelector("#replies");
    replies.appendChild(newReply);
    newReply.classList.remove("hidden")
    replyTextareaDiv.children[0].value = "";
}
