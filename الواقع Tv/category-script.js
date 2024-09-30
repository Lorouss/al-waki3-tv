document.addEventListener('DOMContentLoaded', function() {
    const newsContent = document.getElementById('news-content');
    const pagination = document.getElementById('pagination');
    let newsCards = Array.from(document.querySelectorAll('.news-card')); // تحويل NodeList إلى Array
    let currentPage = 1;
    const cardsPerPage = 4; // عدد البطاقات لكل صفحة
    const maxPagesToShowAfter = 1; // عدد الصفحات التي سيتم عرضها بعد الصفحة الحالية

    // إعادة ترتيب البطاقات بحيث تكون البطاقة الأخيرة المضافة في الصفحة الأولى
    newsCards.reverse(); // عكس ترتيب البطاقات ليكون آخر بطاقة أضيفت هي الأولى في العرض

    // إعادة ترتيب عرض البطاقات في الواجهة
    newsContent.innerHTML = ''; // إزالة البطاقات الحالية
    newsCards.forEach(card => newsContent.appendChild(card)); // إضافة البطاقات المرتبة

    function displayCards(page) {
        const start = (page - 1) * cardsPerPage;
        const end = Math.min(start + cardsPerPage, newsCards.length);
        
        newsCards.forEach((card, index) => {
            if (index >= start && index < end) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    function setupPagination() {
        pagination.innerHTML = '';
        const pageCount = Math.ceil(newsCards.length / cardsPerPage);

        // إضافة زر السابق إذا لزم الأمر
        if (currentPage > 1) {
            const prevButton = createPaginationButton('السابق', currentPage - 1);
            pagination.appendChild(prevButton);
        }

        // إضافة أزرار الصفحات
        let startPage = Math.max(1, currentPage - maxPagesToShowAfter); // بداية الصفحات المعروضة بعد الصفحة الحالية
        let endPage = Math.min(startPage + maxPagesToShowAfter * 2, pageCount); // نهاية الصفحات المعروضة بعد الصفحة الحالية

        for (let i = startPage; i <= endPage; i++) {
            const button = createPaginationButton(i, i);
            if (i === currentPage) {
                button.classList.add('active');
            }
            pagination.appendChild(button);
        }

        // إضافة نقاط والصفحة الأخيرة إذا كان هناك صفحات بعد الصفحات المعروضة
        if (endPage < pageCount) {
            const dotsAfter = document.createElement('span');
            dotsAfter.innerText = '...';
            pagination.appendChild(dotsAfter);

            const lastButton = createPaginationButton(pageCount, pageCount);
            pagination.appendChild(lastButton);
        }

        // إضافة زر التالي إذا لزم الأمر
        if (currentPage < pageCount) {
            const nextButton = createPaginationButton('التالي', currentPage + 1);
            pagination.appendChild(nextButton);
        }

        displayCards(currentPage); // عرض البطاقات للصفحة الحالية عند التحميل
    }

    function createPaginationButton(text, page) {
        const button = document.createElement('button');
        button.innerText = text;
        button.addEventListener('click', function() {
            currentPage = page;
            displayCards(currentPage);
            setupPagination(); // إعادة إعداد الأزرار بناءً على الصفحة الحالية
        });
        return button;
    }

    // إعداد التصفح عند تحميل الصفحة
    setupPagination();

    // إضافة الحدث لفتح المقال في صفحة جديدة
    newsCards.forEach(card => {
        card.addEventListener('click', function(event) {
            const articleUrl = card.getAttribute('data-src');
            const herf = card.getAttribute('herf');

            if (herf) {
                window.open(herf, '_blank'); // فتح الرابط المحدد إذا كانت هناك قيمة لل herf
            } else {
                openArticleModal(articleUrl); // فتح المقال كما هو معمول به
            }
        });
    });

    // فتح المقال في صفحة جديدة
    function openArticleModal(url) {
        const modalWindow = window.open(`news.html?url=${encodeURIComponent(url)}`, '_blank');
        if (modalWindow) {
            modalWindow.focus();
        } else {
            alert('يرجى تمكين النوافذ المنبثقة في المتصفح الخاص بك لعرض المقال.');
        }
    }
});

