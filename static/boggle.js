"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;

/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // console.log(board);
  let size = board.length;
  let $tbody = $("<tbody>");

  // Create a table for the size of the board, adding in the letters at the correct point.
  for (let i = 0; i < size; i++) {
    let $row = $("<tr>")
      for (let j = 0; j < size; j++) {
        let $cell = $(`<td>${board[i][j]}</td>`);
        $row.append($cell);
      }
      $tbody.append($row);
  }
  $table.append($tbody);

  // loop over board and create the DOM tr/td structure
}

start();

async function handleFormSubmission(evt) {
  //form submission, takes in a word and checks if it is a word
  evt.preventDefault();

  let word = $wordInput.val();
  await checkWord(word);

  $wordInput.val("");
}

$form.on("submit", handleFormSubmission);

async function checkWord(word) {
  //check if a word is an english word and is in the boggle board then makes a message to display
  let resp = await axios({
    url: "/api/score-word",
    method: "POST",
    data: {
      word,
      gameId
    }
  });

  let result = resp.data;

  if (result.result === "ok") {
    addCorrectWord(word);
  } else {
    badPlayMessage();
  }
  return result;
}

function badPlayMessage() {
  //display that their word was not legal
  $message.empty();
  $message.append("that is not a legal play");
}

function addCorrectWord(word) {
  //display their word in the list of played words.
  $message.empty();
  $playedWords.append(`<li>${word}</li>`);
}
//console.assert(condition, string message)
//throws an error
