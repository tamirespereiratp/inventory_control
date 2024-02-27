jQuery(function() {
    const $modal = $("#suppliersModal");

    $modal.on("show.bs.modal", function(e) {
        const $button = $(e.relatedTarget); // Botão que acionou o modal
        const url = $button.data("url"); // Extrai o ID do produto do atributo data
      
        fetch(url)
            .then(response => response.json())
            .then(suppliers => {
                // Implemente a criação de uma tabela com nome e preço de custo de cada fornecedor
                const $suppliersTableBody = $("#suppliersTableBody");
                $suppliersTableBody.empty(); // Limpa a tabela existente

                suppliers.forEach(supplier => {
                    // Cria uma nova linha para cada fornecedor
                    const $row = $("<tr></tr>");
                    $row.append($("<td>").text(supplier.name));
                    $row.append($("<td>").text(supplier.cost_price));

                    // Adiciona a linha à tabela
                    $suppliersTableBody.append($row);
                });
            })
            .catch(console.error);
    });
});