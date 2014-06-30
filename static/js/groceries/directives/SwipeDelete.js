Groceries.directive('swipeDelete', ['$swipe', function ($swipe) {
    return {
        restrict: 'A',
        scope: {},
        link: function (scope, element, attrs) {
            var swipeHandlers = {};

            swipeHandlers.move = function (coords) {
                var x = coords.x - element[0].offsetLeft;

                if (x > element[0].clientWidth) {
                    x = element[0].clientWidth;
                }

                element.addClass('swipe-delete-active');
                element.find('span').css('width', x + 'px');
            };

            swipeHandlers.end = function (coords) {
                element.removeClass('swipe-delete-active');
                element.find('span').css('width', '');
            };

            $swipe.bind(element, swipeHandlers);
        }
    };
}]);
