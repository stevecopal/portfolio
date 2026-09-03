/* ═══════════════════════════════════════════════════════
   SHADOW DOORS — Page Transition Manager
   ═══════════════════════════════════════════════════════ */
(function() {
    'use strict';

    var EASING = 'cubic-bezier(0.16, 1, 0.3, 1)';
    var EASING_MICRO = 'cubic-bezier(0.4, 0, 0.1, 1)';
    var DOOR_CLOSE_DURATION = 350;
    var DOOR_OPEN_DURATION = 550;
    var SIGNAL_DURATION = 200;
    var TOTAL_CLOSE = 500;
    var TOTAL_OPEN = 700;

    var isTransitioning = false;
    var doors, doorLeft, doorRight, signalLine, signalDot;
    var labelText, labelDest;

    function init() {
        doors = document.querySelector('.shadow-doors');
        if (!doors) return;

        doorLeft = doors.querySelector('.shadow-doors__left');
        doorRight = doors.querySelector('.shadow-doors__right');
        signalLine = doors.querySelector('.shadow-doors__signal-line');
        signalDot = doors.querySelector('.shadow-doors__signal-dot');
        labelText = doors.querySelector('.shadow-doors__label-text');
        labelDest = doors.querySelector('.shadow-doors__label-dest');

        interceptLinks();
        handlePopState();
        initPageLoader();
        initPageEnter();
    }

    /* ── PAGE LOADER ─────────────────────────────────────── */
    function initPageLoader() {
        var loader = document.querySelector('.page-loader');
        if (!loader) return;

        var minDisplay = 1000;
        var startTime = Date.now();

        function hideLoader() {
            var elapsed = Date.now() - startTime;
            var remaining = Math.max(0, minDisplay - elapsed);

            setTimeout(function() {
                loader.classList.add('loaded');
                document.body.classList.remove('is-loading');
                setTimeout(function() {
                    loader.remove();
                }, 500);
            }, remaining);
        }

        if (document.readyState === 'complete') {
            hideLoader();
        } else {
            window.addEventListener('load', hideLoader);
        }
    }

    /* ── PAGE ENTER ANIMATION ────────────────────────────── */
    function initPageEnter() {
        var content = document.querySelector('.page-content');
        if (!content) return;

        content.classList.add('is-entering');

        var elements = content.querySelectorAll('[data-reveal-element]');
        if (!elements.length) {
            content.classList.remove('is-entering');
            return;
        }

        requestAnimationFrame(function() {
            requestAnimationFrame(function() {
                elements.forEach(function(el) {
                    el.classList.add('reveal-ready');
                });

                setTimeout(function() {
                    content.classList.remove('is-entering');
                }, 800);
            });
        });
    }

    /* ── LINK INTERCEPTION ───────────────────────────────── */
    function interceptLinks() {
        document.addEventListener('click', function(e) {
            var link = e.target.closest('a');
            if (!link) return;

            if (shouldIntercept(link, e)) {
                e.preventDefault();
                e.stopPropagation();

                if (isTransitioning) return;

                var href = link.getAttribute('href');
                var transitionType = link.getAttribute('data-transition') || 'page';
                var label = link.getAttribute('data-transition-label') || '';

                startTransition(href, transitionType, label, link);
            }
        }, true);
    }

    function shouldIntercept(link, e) {
        // Don't intercept if already transitioning
        if (isTransitioning) return false;

        var href = link.getAttribute('href');
        if (!href) return false;

        // Skip anchors (handled by smooth scroll)
        if (href.charAt(0) === '#') return false;

        // Skip external links
        if (href.indexOf('http') === 0 && href.indexOf(window.location.origin) !== 0) return false;

        // Skip mailto, tel
        if (href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) return false;

        // Skip download links
        if (link.hasAttribute('download')) return false;

        // Skip target="_blank"
        if (link.getAttribute('target') === '_blank') return false;

        // Skip modifier keys (Ctrl/Cmd/Shift/Alt)
        if (e && (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey)) return false;

        // Skip middle click
        if (e && e.button !== 0 && e.button !== undefined) return false;

        // Skip right click
        if (e && e.button === 2) return false;

        // Skip if data-transition="none"
        if (link.getAttribute('data-transition') === 'none') return false;

        // Skip pagination links (let them work normally to avoid complications)
        if (href.indexOf('?page=') !== -1 || href.indexOf('&page=') !== -1) return false;

        // Skip tech filter links
        if (href.indexOf('?tech=') !== -1) return false;

        // Same origin check
        try {
            var url = new URL(href, window.location.origin);
            if (url.origin !== window.location.origin) return false;
        } catch(err) {
            return false;
        }

        // Skip if same page
        var currentPath = window.location.pathname;
        var targetPath = new URL(href, window.location.origin).pathname;
        if (currentPath === targetPath) return false;

        return true;
    }

    /* ── TRANSITION ORCHESTRATION ────────────────────────── */
    function startTransition(href, type, label, clickedElement) {
        isTransitioning = true;

        // Block scroll
        document.body.style.overflow = 'hidden';

        // Set label
        if (labelText) labelText.textContent = label || '';
        if (labelDest) labelDest.textContent = '';

        // Phase 1: Click response (micro-interaction on clicked element)
        if (clickedElement) {
            clickedElement.style.transform = 'scale(0.98)';
            setTimeout(function() {
                clickedElement.style.transform = '';
            }, 150);
        }

        // Phase 2: Page exit animation
        var content = document.querySelector('.page-content');
        if (content) {
            content.classList.add('is-exiting');
        }

        // Phase 3: Shadow Doors close
        setTimeout(function() {
            closeDoors(function() {
                // Phase 4: Green signal
                showSignal(function() {
                    // Phase 5: Navigate
                    navigateTo(href);
                });
            });
        }, 120);
    }

    /* ── DOORS CLOSE ─────────────────────────────────────── */
    function closeDoors(callback) {
        doors.classList.add('active');

        // Left door - arrives first
        doorLeft.style.transition = 'transform ' + DOOR_CLOSE_DURATION + 'ms ' + EASING;
        doorLeft.style.transform = 'translateX(0)';

        // Right door - 40ms delay
        setTimeout(function() {
            doorRight.style.transition = 'transform ' + DOOR_CLOSE_DURATION + 'ms ' + EASING;
            doorRight.style.transform = 'translateX(0)';
        }, 40);

        // Wait for both doors to settle
        setTimeout(callback, DOOR_CLOSE_DURATION + 80);
    }

    /* ── GREEN SIGNAL ────────────────────────────────────── */
    function showSignal(callback) {
        // Show signal container
        doors.querySelector('.shadow-doors__signal').style.opacity = '1';

        // Animate line height
        signalLine.style.transition = 'height ' + SIGNAL_DURATION + 'ms ' + EASING;
        signalLine.style.height = '60px';

        // Animate dot
        setTimeout(function() {
            signalDot.style.transition = 'opacity 0.15s ease, transform 0.15s ease';
            signalDot.style.opacity = '1';
            signalDot.style.transform = 'scale(1)';
        }, SIGNAL_DURATION * 0.4);

        // Callback after signal
        setTimeout(function() {
            // Fade signal
            signalLine.style.transition = 'opacity 0.15s ease';
            signalLine.style.opacity = '0';
            signalDot.style.opacity = '0';

            setTimeout(callback, 150);
        }, SIGNAL_DURATION + 100);
    }

    /* ── NAVIGATION ──────────────────────────────────────── */
    function navigateTo(href) {
        // Update URL
        if (history.pushState) {
            history.pushState({ sdTransition: true }, '', href);
        }

        // Scroll to top
        window.scrollTo(0, 0);

        // Fetch new page
        fetch(href, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'text/html'
            }
        }).then(function(response) {
            if (!response.ok) throw new Error('Navigation failed');
            return response.text();
        }).then(function(html) {
            applyNewPage(html, href);
        }).catch(function() {
            // Fallback: normal navigation
            window.location.href = href;
        });
    }

    /* ── APPLY NEW PAGE ──────────────────────────────────── */
    function applyNewPage(html, href) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');

        var newContent = doc.querySelector('.page-content');
        var currentContent = document.querySelector('.page-content');

        if (!newContent || !currentContent) {
            window.location.href = href;
            return;
        }

        // Replace content
        currentContent.innerHTML = newContent.innerHTML;

        // Update title
        var newTitle = doc.querySelector('title');
        if (newTitle) document.title = newTitle.textContent;

        // Update meta tags
        var newMetas = doc.querySelectorAll('meta[property], meta[name="description"]');
        newMetas.forEach(function(meta) {
            var existing = document.querySelector('meta[property="' + meta.getAttribute('property') + '"]') ||
                          document.querySelector('meta[name="' + meta.getAttribute('name') + '"]');
            if (existing) {
                existing.setAttribute('content', meta.getAttribute('content'));
            }
        });

        // Re-initialize page-specific scripts
        reinitializePageScripts(doc);

        // Reset scroll
        document.body.style.overflow = '';
        window.scrollTo(0, 0);

        // Open doors
        openDoors(function() {
            isTransitioning = false;

            // Initialize page enter animation
            initPageEnter();

            // Re-init interactions
            if (window.InteractionManager) {
                window.InteractionManager.reinit();
            }
        });
    }

    /* ── DOORS OPEN ──────────────────────────────────────── */
    function openDoors(callback) {
        doors.classList.add('active');

        // Left door opens
        doorLeft.style.transition = 'transform ' + DOOR_OPEN_DURATION + 'ms ' + EASING;
        doorLeft.style.transform = 'translateX(-100%)';

        // Right door opens - slightly faster
        setTimeout(function() {
            doorRight.style.transition = 'transform ' + (DOOR_OPEN_DURATION - 60) + 'ms ' + EASING;
            doorRight.style.transform = 'translateX(100%)';
        }, 30);

        // Reset signal
        signalLine.style.height = '0';
        signalLine.style.opacity = '1';
        signalDot.style.opacity = '0';
        signalDot.style.transform = 'scale(0)';
        doors.querySelector('.shadow-doors__signal').style.opacity = '0';

        setTimeout(function() {
            doors.classList.remove('active');
            callback();
        }, DOOR_OPEN_DURATION + 80);
    }

    /* ── REINITIALIZE PAGE SCRIPTS ───────────────────────── */
    function reinitializePageScripts(doc) {
        // Re-init project filters if on projects page
        if (typeof initProjectFilters === 'function') {
            initProjectFilters();
        }

        // Re-init contact form if on contact page
        if (typeof initContactForm === 'function') {
            initContactForm();
        }

        // Re-init lightbox on project detail pages
        var zoomables = document.querySelectorAll('.pd-frame img, .pd-shot-media img');
        if (zoomables.length && typeof openLightbox !== 'undefined') {
            zoomables.forEach(function(img) {
                img.style.cursor = 'zoom-in';
                img.addEventListener('click', function() { openLightbox(img); });
            });
        }

        // Re-run hero.js if present
        var heroScript = doc.querySelector('script[src*="hero.js"]');
        if (heroScript) {
            var newScript = document.createElement('script');
            newScript.src = heroScript.src;
            document.body.appendChild(newScript);
        }

        // Re-run tech-background.js if present
        var techBgScript = doc.querySelector('script[src*="tech-background.js"]');
        if (techBgScript) {
            var newTechScript = document.createElement('script');
            newTechScript.src = techBgScript.src;
            document.body.appendChild(newTechScript);
        }
    }

    /* ── BACK/FORWARD BUTTON ─────────────────────────────── */
    function handlePopState() {
        window.addEventListener('popstate', function(e) {
            if (isTransitioning) return;

            // If it was a SD transition, don't replay animation
            if (e.state && e.state.sdTransition) {
                // Just reload the page content
                isTransitioning = true;
                document.body.style.overflow = 'hidden';

                closeDoors(function() {
                    window.location.reload();
                });
                return;
            }

            // Normal back/forward - let the browser handle it
        });
    }

    /* ── INIT ────────────────────────────────────────────── */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for external access
    window.ShadowDoors = {
        navigate: function(href, label) {
            if (!isTransitioning) {
                startTransition(href, 'page', label || '');
            }
        },
        isTransitioning: function() { return isTransitioning; }
    };

})();
