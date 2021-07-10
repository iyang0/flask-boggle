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
  let tbody = $("<tbody>");
  
  // Create a table for the size of the board, adding in the letters at the correct point.
  for(let i=0;i<size;i++){
    let row = $("<tr>")
    for(let j=0;j<size;j++){
        let cell = $(`<td>${board[i][j]}</td>`);
        row.append(cell);
    }
    tbody.append(row);
  }
  $table.append(tbody);
  
  // loop over board and create the DOM tr/td structure
}


start();