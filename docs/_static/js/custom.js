document.addEventListener('DOMContentLoaded', function(){
    var x = document.getElementsByClassName("pylib-comparison");
    if (x.length == 1) {
        feature_table = x[0];
        var cells = feature_table.getElementsByTagName("td");
        for (var i = 0; i < cells.length; i++) {
            var content = cells[i].innerHTML;
            console.log(content);
            if (content === "Yes") {
                cells[i].classList.add('feature_yes')
            }
            else if (content == "No") {
                cells[i].classList.add('feature_no')
            }
        }
    }
}, false);
