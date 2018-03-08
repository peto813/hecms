var hmShipFilters = angular.module('hmShipFilters',[]);

hmShipFilters.filter('capitalize', function() {
    return function(input) {
      return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    }
});

hmShipFilters.filter('capfirstlettereachword', function() {
    return function(input) {
    	if (input){
            var splitStr = input.toLowerCase().split(' ');
            for (var i = 0; i < splitStr.length; i++) {
                splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
            }
            return splitStr.join(' ');   		
    	}

    };
})

hmShipFilters.filter('separateNumberLetter', function() {
    return function(input) {
        var str = String(input);
        str = str.replace(/(\d+)/g, function (_, num){
            //console.log(num);
            return ' ' + num + ' ';
        });
        str = str.trim();
        return str;
    };
})
