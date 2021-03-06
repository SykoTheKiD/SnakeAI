//direction in which the snake is moving
var directionString = 'right';
var lastDirectionString = null;

var foodItems = [];
var stopMovingOfSnake = false;
var snake = [];
var snakeSpeed = 40;

var gameFinished = false;

//dynamic styles for the icons relating on the screen properties
var itemWidth = null;
var itemHeight = null;

$(function () {    
    var fieldSize = 32;    
    //calculate the field width and height which is depending on the monitor resolution and the items
    var width = (Math.round($(document).width() / fieldSize) * fieldSize) - fieldSize;
    var height = (Math.round($(document).height() / fieldSize) * fieldSize) - fieldSize;

    var leftPos = ($(document).width() - width) / 2;
    var topPos = ($(document).height() - height) / 2;

    $('#field').css({
        "width": width,
        "height": height,
        "left": leftPos,
        "top": topPos
    });

    createSnake();
    pauseSnake()
    $(document).keyup(function (e) {
        if (e.keyCode == 27 || e.keyCode == 32) { //Esc or Space
            stopMovingOfSnake ? continueSnake() : pauseSnake();
        }
    });
});

//creates the parts of the snake
function createSnake() {
    var array_snake_parts = [];
    
    //Create the head
    var snake_head = $('<div></div>', {
        "class": "snake-head"
    });
    array_snake_parts.push(snake_head);
    //Create the tail parts    
    var amountOfPartsByDefault = Math.floor(Math.random() * (21));

    for (var z = 0; z < amountOfPartsByDefault; z++) {
        var snake_tail = $('<div></div>', {
            "class": "snake-tail"
        });
        array_snake_parts.push(snake_tail);
    }

    snake = array_snake_parts;

    stimulateSnake();
}

function stimulateSnake() {
    //set the snake onto the field
    for (var z = 0; z < snake.length; z++) {
        var part = snake[z];

        $('#field').append(part);

        itemWidth = $(part).outerWidth();
        itemHeight = $(part).outerHeight();
    }
    moveSnake();
    createFood();
}

//move the snake
function moveSnake() {
    var myFunction = function () {
        if (stopMovingOfSnake) return false;
        var position = null;

        for (var z = 0; z < snake.length; z++) {
            var part = snake[z];                                                
            
            //head part moves into the directionString
            if (z === 0) {
                position = part.position();

                if (directionString === 'left') {
                    $(part).css({
                        left: position.left - part.outerWidth()
                    });
                } else if (directionString === 'up') {
                    $(part).css({
                        top: position.top - part.outerHeight()
                    });
                } else if (directionString === 'right') {
                    $(part).css({
                        left: position.left + part.outerWidth()
                    });
                } else if (directionString === 'down') {
                    $(part).css({
                        top: position.top + part.outerHeight()
                    });
                }
                lastDirectionString = directionString;
                
                //check if the position of the head is out of allowed area
                checkNewPosition();
            } else {
                var nextPosition = part.position();
                $(part).css({
                    left: position.left,
                    top: position.top
                });
                position = nextPosition;
            }
        }
        clearInterval(interval);
        interval = setInterval(myFunction, snakeSpeed);
    }
    var interval = setInterval(myFunction, snakeSpeed);

    setMoveEvents();
}

function setMoveEvents() {
    //Change the direction in which the snake will move
    $('body').on('keydown', function (e) {
        //Arrow keycodes
        if (e.which === 37 && lastDirectionString !== 'right') {
            directionString = 'left';
        } else if (e.which === 38 && lastDirectionString !== 'down') {
            directionString = 'up';
        } else if (e.which === 39 && lastDirectionString !== 'left') {
            directionString = 'right';
        } else if (e.which === 40 && lastDirectionString !== 'up') {
            directionString = 'down';
        }
    });
}

//check if the new position of the head is valid to continue moving
function checkNewPosition() {
    var head = snake[0];
    var position = head.position();        
    
    //check if snake is out the field
    if (position.left < 0 ||
        position.top < 0 || 
        position.left + head.outerWidth() > $('#field').outerWidth() || 
        position.top + head.outerHeight() > $('#field').outerHeight()) {
        showInfoAlert('<h4>Game over!</h4><br/>Highscore: ' + snake.length + '<br/><br/><a href="#" onclick="location.reload();" onkeydown="javascript: if(event.keyCode == 13) location.reload();">Start new game!</a>');
        $('#infoAlert a').focus();
        stopMovingOfSnake = true;
        killSnake();
    }
    
    //check if head is over a part of the tail
    for (var z = 1; z < snake.length; z++) {
        var part = snake[z];
        if (head.position().top === part.position().top && head.position().left === part.position().left) {
            showInfoAlert('<h4>Game over!</h4><br/>Highscore: ' + snake.length + '<br/><br/><a href="#" onclick="location.reload();" onkeydown="javascript: if(event.keyCode == 13) location.reload();">Start new game!</a>');
            //focus link for key event
            $('#infoAlert a').focus();
            stopMovingOfSnake = true;
            killSnake();
        }
    }    
    
    //eat the food
    for (var z = 0; z < foodItems.length; z++) {
        var item = foodItems[z];
        if (Math.abs(head.position().top - item.position().top) < 10 && Math.abs(head.position().left - item.position().left) < 10) {
            //delete the item
            $(item).remove();
            
            //add part to the tail
            var snake_tail = $('<div></div>', {
                "class": "snake-tail"
            });
            snake.push(snake_tail);
            $('#field').append(snake_tail);
            foodItems.pop();
            createFood();
        }
    }
}

function pauseSnake() {
    stopMovingOfSnake = true;
    showInfoAlert('Game paused');
    $('#field').css('background-color', "#70a6ff")
}
function continueSnake() {
    if (gameFinished) return false;
    stopMovingOfSnake = false;
    hideInfoAlert();
    $('#field').css('background-color', "#121312")
}

function killSnake() {
    gameFinished = true;

    $('.snake-tail').addClass('animated jello');
    $('.snake-head').addClass('animated jello');

    setTimeout(function () {
        $('.snake-tail').addClass('bounceOutLeft');
        $('.snake-head').addClass('bounceOutLeft');
    }, 400);

    $('#field').css('background-color', "#ff0000")
}

function showInfoAlert(text) {
    $('#infoAlert').html(text).show().addClass('bounceIn');
}
function hideInfoAlert() {
    $('#infoAlert').hide().removeClass('bounceIn');
}

function createFood() {
    var position = generateFieldPosition();
    var foodItem = $('<div></div>', {
        "class": "food",
        "css": {
            "left": position.left,
            "top": position.top
        }
    });

    $('#field').append(foodItem);
    foodItems.push(foodItem);
}

//generates top and left position for a item to set it onto the field
function generateFieldPosition() {
    //calculate max amount of vertical fields for items
    var vertAmount = Math.round(($('#field').innerWidth() - itemWidth) / itemWidth);
    
    //calculate max amount of horizontal fields for items
    var horAmount = Math.round(($('#field').innerHeight() - itemHeight) / itemHeight);

    var left = null;
    var top = null;
    generateLeftAndTop();

    while (checkIfOnSnake()) {
        generateLeftAndTop();
    }

    function checkIfOnSnake() {
        for (var z = 0; z < snake.length; z++) {
            var snakePart = snake[z];

            if (snakePart.position().left === left && snakePart.position().top === top) {
                return true;
            }
        }
        return false;
    }

    function generateLeftAndTop() {
        left = Math.round(generateValues(0, vertAmount)) * itemWidth;
        top = Math.round(generateValues(0, horAmount)) * itemHeight;
    }

    return {
        "left": left,
        "top": top
    };
}

//Generates some random values between min and max
function generateValues(min, max) {
    return Math.random() * (max - min) + min; //returns float
}