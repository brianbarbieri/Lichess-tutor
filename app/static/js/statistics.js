function changeTree(){ 
    $.getJSON('/tree_data', {
        move: this.innerHTML.replace(/\s/g, ""),
    }, function(data) {
        $('.moverow').remove();
        var i = 1;
        for (var move in data) {
            content = `
            <tr class="moverow">
                <td class='move'>${move}</td>
                <td>
                    <div id="chart${i}"></div>
                    <script>
                        var sampleData = [
                            { label: "won", value: ${data[move]["score"]["won"]} },
                            { label: "tie", value: ${data[move]["score"]["tie"]} },
                            { label: "lost", value: ${data[move]["score"]["lost"]} }
                        ] 
                        stackedBar("#chart${i}", sampleData)
                    </script>
                </td>
                <td>
                    ${data[move]["score"]["won"] + data[move]["score"]["won"] + data[move]["score"]["won"]}
                </td>
            </tr>`;
            $(".movelist").append(content);
            i++;
        }
        $(".movelist").append("<script>$('.move').click(changeTree);</script>");
    });       
}


$('.move').click(changeTree);