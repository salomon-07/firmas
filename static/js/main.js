document.addEventListener('DOMContentLoaded', () => {
    // Dynamic Rows Table
    const btnAddRow = document.getElementById('btnAddRow');
    const tableBody = document.querySelector('#tableEquipos tbody');

    if (btnAddRow) {
        btnAddRow.addEventListener('click', () => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><input type="text" name="equipo[]" required></td>
                <td><input type="text" name="marca[]" required></td>
                <td><input type="text" name="modelo[]" required></td>
                <td><input type="text" name="serie[]" required></td>
                <td><input type="text" name="estado[]" value="usada" required></td>
                <td><button type="button" class="btn-delete" onclick="removeRow(this)">X</button></td>
            `;
            tableBody.appendChild(row);
        });
    }

    // Canvas Signature Logic
    const canvas = document.getElementById('signatureCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let isDrawing = false;

        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 2;

        function getPos(e) {
            const rect = canvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return {
                x: clientX - rect.left,
                y: clientY - rect.top
            };
        }

        function startDrawing(e) {
            isDrawing = true;
            const pos = getPos(e);
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y);
        }

        function draw(e) {
            if (!isDrawing) return;
            e.preventDefault();
            const pos = getPos(e);
            ctx.lineTo(pos.x, pos.y);
            ctx.stroke();
        }

        function stopDrawing() {
            if (isDrawing) {
                isDrawing = false;
                // Save signature image to hidden field
                document.getElementById('firmaBase64').value = canvas.toDataURL();
            }
        }

        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseleave', stopDrawing);

        canvas.addEventListener('touchstart', startDrawing);
        canvas.addEventListener('touchmove', draw);
        canvas.addEventListener('touchend', stopDrawing);

        document.getElementById('btnClearSignature').addEventListener('click', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            document.getElementById('firmaBase64').value = '';
        });
    }
});

function removeRow(btn) {
    const row = btn.closest('tr');
    if (document.querySelectorAll('#tableEquipos tbody tr').length > 1) {
        row.remove();
    } else {
        alert('Debe conservar al menos un registro.');
    }
}