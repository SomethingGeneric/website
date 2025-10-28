const table = document.querySelector('#main-content table');

if (table) {
  const courseCells = table.querySelectorAll('tbody tr td:nth-child(6)');

  courseCells.forEach((cell) => {
    if (cell.dataset.coursesEnhanced === 'true') {
      return;
    }

    const rawHtml = (cell.innerHTML || '').trim();
    if (!rawHtml) {
      cell.dataset.coursesEnhanced = 'true';
      return;
    }

    const normalized = rawHtml.replace(/<br\s*\/?>/gi, ' ');
    const codeMatches = normalized.match(/\b[A-Z]{3}-\d{3}\b/g);
    if (!codeMatches) {
      cell.dataset.coursesEnhanced = 'true';
      return;
    }

    const codes = [];
    codeMatches.forEach((code) => {
      const trimmed = code.trim();
      if (trimmed && !codes.includes(trimmed)) {
        codes.push(trimmed);
      }
    });

    if (!codes.length) {
      cell.dataset.coursesEnhanced = 'true';
      return;
    }

    const details = document.createElement('details');
    details.className = 'courses-collapse';

    const summary = document.createElement('summary');
    const count = codes.length;
    const plural = count === 1 ? '' : 's';
    const label = `${count} course${plural}`;

    const updateSummary = () => {
      summary.textContent = details.open ? `Hide ${label}` : `Show ${label}`;
    };

    updateSummary();
    details.addEventListener('toggle', updateSummary);

    const list = document.createElement('ul');
    list.className = 'courses-list';

    codes.forEach((code) => {
      const item = document.createElement('li');
      item.textContent = code;
      list.append(item);
    });

    details.append(summary, list);

    cell.textContent = '';
    cell.append(details);
    cell.dataset.coursesEnhanced = 'true';
  });
}
