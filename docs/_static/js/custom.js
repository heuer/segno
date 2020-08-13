document.addEventListener('DOMContentLoaded', function(){
    var x = document.getElementsByClassName("pylib-comparison");
    if (x.length == 1) {
        feature_table = x[0];
        var cells = feature_table.getElementsByTagName("td");
        for (var i = 0; i < cells.length; i++) {
            var content = cells[i].innerHTML;
            if (content.includes("Yes")) {
                cells[i].classList.add('feature_yes')
            }
            else if (content.includes("No")) {
                cells[i].classList.add('feature_no')
            }
        }
    }
}, false);
