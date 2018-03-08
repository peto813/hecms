var hmShipDirectives = angular.module('hmShipDirectives',[]);


hmShipDirectives.directive("fileread", [function () {
    return {
        scope: {
            fileread: "="
        },
        link: function (scope, element, attributes) {

            element.bind("change", function (changeEvent) {
                var reader = new FileReader();
                reader.onload = function (loadEvent) {
                    scope.$apply(function () {
                        scope.fileread = loadEvent.target.result;
                        console.log(scope.fileread)
                    });
                }
                reader.readAsDataURL(changeEvent.target.files[0]);
            });
        }
    }
}]);


hmShipDirectives.directive('validationElement', function() {

      var directive = {};
      directive.restrict = 'E';
      directive.scope = false;
      directive.templateUrl = '/static/templates/userapp/directiveTemplates/validationTemplate.html';
      return directive;
});

hmShipDirectives.directive('tabElement', function($location) {

      var directive = {};
      directive.restrict = 'E';
      directive.scope = {
        'tabList' : '='
      };
      directive.templateUrl = '/static/templates/userapp/directiveTemplates/tabElement.html';
      directive.link = function ( scope, element, attributes, ngModel ) {

          scope.currentUrl = $location.url()
      };
      return directive;
});




hmShipDirectives.directive('loading', ['$http', function ($http) {
    return {
        restrict: 'A',
        scope:true,
        link: function (scope, elm, attrs) {
            scope.isLoading = function () {
                return $http.pendingRequests.length > 0;
            };
            scope.$watch(scope.isLoading, function (v) {
                if (v) {
                    elm.css('visibility', 'visible');
                } else {
                    elm.css('visibility', 'hidden');

                }
                //scope.$apply();
            });
        }
    };
}]);



hmShipDirectives.directive('panelTable', function() {

      var directive = {};
      directive.restrict = 'E';
      //directive.transclude = true;
      directive.transclude= {
          //'labelAddon': '?labelAddon',
          extra: '?extraElement'
      };
      directive.scope = {
          panelTitle : '@',
          //searchDateField: "@",
          minDate : '=?',
          maxDate : '=?',
          tableData : '=?',
          tableSearch: '=?',
          placeholder :'@?',
          advancedSearch : '=?',
          advSearchFn: '&?',
          typeAheadModel: '=?'
      };
      //directive.controller = 'orderBookController'
      // directive.link = function(scope, element, attributes, ngModel, transclude ) { 
        
      //   transclude( function(clone, scope) {
      //     console.log(scope.dateRange)
      //     scope.dateRange.setViewValue('months-6')
      //     //element.append(clone);
      //   })
      // }
      directive.templateUrl = '/static/templates/userapp/directiveTemplates/dataTableTemplate.html';
      return directive;
});


hmShipDirectives.directive("yearMonthInput", function() {

           var directive = {};
           directive.restrict = 'E';
           directive.transclude = true;
           directive.scope = {
              minDate : '=',
              maxDate : '='
           };
           directive.require = 'ngModel';
           directive.templateUrl = '/static/templates/userapp/directiveTemplates/yearmonthpicker.html';
           directive.link = function(scope, element, attributes, ngModel) {
            function dateInCalendarRange(minDate, maxDate, dateObj){
              var maxCalendarDate = new Date(maxDate.getFullYear(), maxDate.getMonth()+1, 0);
              var minCalendarDate = new Date(minDate.getFullYear(), minDate.getMonth(), 1)
              if ( (dateObj>=minCalendarDate) && (dateObj <= maxCalendarDate)){
                return true;
              }else{
                return false;
              }
            }

              //ENABLES AND DISABLES THE MONTH AND YEAR
              scope.dateCheck= function(year, month){
                if( year ) {
                  //THIS IS THE ITERATION TO CHECK AGAINST
                  var date_to_check = new Date(year, month-1, 1);
                  return !dateInCalendarRange(scope.minDate, scope.maxDate, date_to_check );
                }else{
                  return true;
                }
              }

              scope.yearList = function(minDate, maxDate){
                var yearList = [];
                for ( var i = minDate.getFullYear(); i <= maxDate.getFullYear(); i++){
                    yearList.push(i)
                }               
                return yearList;
              }


                scope.monthList = [
                    { 'name': 'January', 'value' : 1 }, 
                    { 'name': 'February', 'value' : 2 },
                    { 'name': 'March', 'value' : 3 },
                    { 'name': 'April', 'value' : 4 },
                    { 'name': 'May', 'value' : 5 },
                    { 'name': 'June', 'value' : 6 },
                    { 'name': 'July', 'value' : 7 },
                    { 'name': 'August', 'value' : 8 },
                    { 'name': 'September', 'value' : 9 },
                    { 'name': 'October', 'value' : 10 },
                    { 'name': 'November', 'value' : 11},
                    { 'name': 'December', 'value' : 12 }
                ];

                scope.dateselect = function(){
                  if(scope.years && scope.months){
                    var selectedDate = new Date(scope.years, scope.months-1, 1);
                    ngModel.$setViewValue(selectedDate);                   
                  }

                }

           }
           return directive;

    });



hmShipDirectives.directive('fieldMatch', function() {

    var directive = {};
    directive.require =  "ngModel";
    //directive.restrict = '';
    directive.scope = {
      otherModelValue: "=compareTo"
    };

    directive.link = function(scope, element, attributes, ngModel) {
             
            ngModel.$validators.fieldMatch = function(modelValue) {
                return modelValue === scope.otherModelValue;
            };
 
            scope.$watch("otherModelValue", function() {
                ngModel.$validate();
            });
    }
    //directive.templateUrl = '/static/templates/userapp/directiveTemplates/validationTemplate.html';
    return directive;

});  


hmShipDirectives.directive('passwordMatch', function() {

    var directive = {};
    directive.require =  "ngModel";
    //directive.restrict = '';
    directive.scope = {
      otherModelValue: "=compareTo"
    };

    directive.link = function(scope, element, attributes, ngModel) {
             
            ngModel.$validators.passwordMatch = function(modelValue) {
                return modelValue === scope.otherModelValue;
            };
 
            scope.$watch("otherModelValue", function() {
                ngModel.$validate();
            });
    }
    //directive.templateUrl = '/static/templates/userapp/directiveTemplates/validationTemplate.html';
    return directive;

});  


hmShipDirectives.directive('lotNumber', function() {

    var directive = {};
    directive.require =  "ngModel";
    directive.restrict = 'E';
    directive.scope = false;

    // directive.link = function(scope, element, attributes, ngModel) {
             
    //         ngModel.$validators.passwordMatch = function(modelValue) {
    //             return modelValue === scope.otherModelValue;
    //         };
 
    //         scope.$watch("otherModelValue", function() {
    //             ngModel.$validate();
    //         });
    // }
    directive.templateUrl = '/static/templates/userapp/directiveTemplates/lotNumberTemplate.html';
    return directive;

});  


hmShipDirectives.directive('textInput', function() {
    var directive = {};
    //directive.require = "^form"
    //directive.require =  "ngModel";
    directive.restrict = 'E';
    directive.transclude= {
        'labelAddon': '?labelAddon',
        'inputAddon': '?inputAddon'
    };
    directive.templateUrl = '/static/templates/userapp/directiveTemplates/textInput.html';
    directive.scope = {
      'name': '@',
      'required': '@',
      'ngModel' : '=',
      'size' : '@',
      'placeholder' : '@',
      'id' : '@',
      'formField': '=',
      'inputDisabled': '=',
      'inputRequired': '=',
      'ngChange' : '&',
      'ngPattern' : '='
    };
    // directive.link=function (scope, element, attrs, form){
    //    scope.peo = scope.ngChange; //save parent form
    // };
    return directive;
});  


hmShipDirectives.directive('selectInput', function() {
    var directive = {};
    //directive.require = "^form"
    directive.require =  "ngModel";
    directive.restrict = 'E';
    directive.transclude= {
        'labelAddon': '?labelAddon',
        'inputAddon': '?inputAddon',
        'inputOptions' : '?inputOptions'
    };
    directive.templateUrl = '/static/templates/userapp/directiveTemplates/selectInput.html';
    directive.scope = {
      'name': '@',
      'required': '@',
      'ngModel' : '=',
      'size' : '@',
      'placeholder' : '@',
      'id' : '@',
      'formField': '=',
      //'selectOptions': '='
    };
    directive.link=function (scope, element, attrs, ngModel ){
      ngModel.$setViewValue(scope.auctionName)
       //scope.form = form; //save parent form
    };
    return directive;
});  

hmShipDirectives.directive('googleMapsAutocomplete', function() {
    var directive = {};
    directive.require =  "ngModel";
    directive.restrict = 'A';
    directive.scope = {
      'googleMapsAutocomplete' :'='
    };

    directive.link = function (scope, element, attrs, ngModel ){

      var placeSearch, autocomplete;
            var componentForm = {
              street_number: 'short_name',
              route: 'long_name',
              locality: 'long_name',
              administrative_area_level_1: 'short_name',
              country: 'long_name',
              postal_code: 'short_name'
            };

      scope.autocomplete = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */(element[0]),
        {types: ['geocode']});

            //REMOVE ENTER KEY 
      google.maps.event.addDomListener(element[0], 'keydown', function(e) { 
        if (e.keyCode == 13) { 
            e.preventDefault(); 
        }
        scope.$apply()
      });



      //autocomplete.addListener('place_changed', fillInAddress);
      google.maps.event.addListener(scope.autocomplete, 'place_changed', function() {
          scope.$apply(function() {
              scope.place = scope.autocomplete.getPlace();
              if(scope.place.geometry){
                var latitude = scope.place.geometry.location.lat();
                var longitude = scope.place.geometry.location.lng();
              }else{
                var latitude = '';
                var longitude = '';
              }

              scope.googleMapsAutocomplete = {
                  latitude:latitude,
                  longitude :longitude
              }
              ngModel.$setViewValue(element.val());
          });
      });

      // google.maps.event.addDomListener(element[0], 'change', function() { 
      //   scope.$apply(function(){
      //    scope.uploadLocationData = false;     
      //   }) 
      // });


      // google.maps.event.addDomListener(element[0], 'change', function() { 
      //   scope.$apply(function(){
      //    scope.uploadLocationData = false;     
      //   }) 
      // });

    };
    return directive;
});  


hmShipDirectives.directive("itemsInList", function() {
    return {
        restrict: "A",
        scope : {
          'itemsInList':'='
        },
        require: "ngModel",
         
        link: function(scope, element, attributes, ngModel) {
            
            ngModel.$validators.itemsInList = function(modelValue) { 
              return (scope.itemsInList.length != 0);
              //return true;
            }
        }
    };
});


hmShipDirectives.directive("carouselOnResize", function($window, $interval, arrayServices) {
    return {
        restrict: "A",
        scope : {
          //elementOnResize:'&?',
          rawGallery:'=carouselOnResize'
        },
        //require: "ngModel",
         
        link: function(scope, element, attributes, ngModel) {
          //scope.rawGallery =[]
          //scope.$digest();

          //NORMALIZE GALLERY ARRAY
          scope.merged = [].concat.apply([], scope.rawGallery);
          scope.width = $window.innerWidth;
          scope.rawGallery = sectionCarousellist(arrayServices.shuffleArray(scope.merged), scope.width);
          
          //FUNCTION THAT SECTIONS THE ARRAY AS PER SCREEN SIZE
          function sectionCarousellist(images, width){
            var param;
            //var images = images
            if(width>=1200){
              param = 5;
            }
            else if(width>=992){
              param = 3;
            }
            else if(width>=768){
              param = 2;
            }
            else if(width>=576){
              param = 0;
            }
            else if(width<576){
              param = 0;
            }
            var range  = 12/(param+1);
            var carousel = [];

            for ( var i=0; i<range; i++ ){
              carousel.push(images.splice(0, param+1))
              //console.log(images.splice(0, range))
            }
            return arrayServices.shuffleArray(carousel);
          }



           angular.element($window).bind('resize', function(){
//scope.rawGallery =[]
//console.log(scope.rawGallery)
            scope.width = $window.innerWidth;
            //RESECTION THE CAROUSEL ON RESIZE
            scope.merged = [].concat.apply([], scope.rawGallery);
            //console.log(scope.merged )
            //console.log(scope.width )
            //console.log(sectionCarousellist(scope.merged, scope.width))
            scope.rawGallery=sectionCarousellist(scope.merged, scope.width);

            //scope.elementOnResize();
            
            //scope.navCollapsed = true
             // manuall $digest required as resize event
             // is outside of angular
             scope.$apply();
           });

        }
    };
});


hmShipDirectives.directive('carouselControls', function() {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      scope.goNext = function() {
        element.isolateScope().next();
      };
      scope.goPrev = function() {
        element.isolateScope().prev();
      };

    }
  };
});


hmShipDirectives.directive("resizeFontToFit", function($window, $timeout) {
    return {
        restrict: "A",
        // scope : {
        //   'resizeFontToFit':'=?'
        // },
        //require: "ngModel",
         
        link: function(scope, element, attributes, ngModel) {

          var fontSize = 28;
          var maxHeight = 40;

          //var getWidth = function() {
            $timeout(function() {
                var fitToWidth = document.getElementById(attributes.resizeFontToFit).getBoundingClientRect().width;
              do {
                  //element.css({fontSize: String(fontSize)+'px',});
                  //element.css('font-size', 8);
                  textHeight = element[0].getBoundingClientRect().height;
                  textWidth = element[0].getBoundingClientRect().width;
                  fontSize = fontSize - 1;

                  //console.log(textWidth)
                  // console.log(fitToWidth)
                  //console.log(fontSize)

            } while ((textHeight > maxHeight || textWidth > fitToWidth) && fontSize > 3);
            //} while (( textWidth > fitToWidth) && fontSize > 3);
              return this;
            });
          //};

          //console.log(attributes)
          
          //console.log( this_width);
          //console.log(fitToWidth);
          // var html = angular.element(element)[0].firstElementChild
          // //var html = element.firstElementChild.innerHTML
          // var line = element.wrapInner( html ).children()[ 0 ]
          // var line = html.innerHTML
          // scope.width = $window.innerWidth;
          //var this_width = element[0];
          //var child_width = element.children()[0].clientWidth;
        //var eleWidth = element.innerWidth();
        //console.log(element[0].offsetWidth);
           //alert(scope.width)
           angular.element($window).bind('resize', function(){

           });

        }
    };
});


hmShipDirectives.directive('pdf', function() {
    return {
        restrict: 'E',
        link: function(scope, element, attrs) {
            var url = scope.$eval(attrs.src);
            console.log(url)
            element.replaceWith('<object width="100%" height="500" style="height: 85vh;" type="application/pdf" data="' + url + '">No Support</object>');
        }
    };
});

