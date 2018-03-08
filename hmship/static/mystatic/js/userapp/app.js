
var hmShipApp = angular.module("hmShipApp",
 [ 
 'ui.router', 
'ui.bootstrap', 
'ngMessages', 
'hmShipControllers', 
'hmShipServices', 
'hmShipDirectives', 
'hmShipFilters',
'ngTouch', 
'ngAnimate', 
'ngFileUpload',
'angular-carousel',
'ngSanitize',
]);
  
 
hmShipApp.config(function($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('editauctionproducts', {
            url:'/editauctionproducts',
            templateUrl : 'static/templates/userapp/auctionproducts/editauctionproducts.html',
            isLogin: true,
            data : { pageTitle: 'Auction Products' },
            controller : 'editProductController',
            resolve: {
                productsList: function($http) {
                    var now_date = new Date()
                    var timestamp_lte = new Date();
                    var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
                    var url = 'api/auctionproducts/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString()
                    var params = { 'q' :  'editproducts'};
                    return $http({ 
                        method: 'GET', 
                        url: url,
                        params: params,
                    }).then(function(response){
                        return response.data;
                    })
                }

            }
        })
        .state('auctionproducts', {
            url:'/auctionproducts',
            templateUrl : 'static/templates/userapp/auctionproducts/uploadauctionproducts.html',
            isLogin: true,
            controller : 'uploadProductController',
            data : { pageTitle: 'Register Auction Products' },
            resolve: {
                auctionList: function($http) {
                    var url = 'api/auctions/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
        })
        .state('about', {
            url:'/about',
            templateUrl : 'static/templates/userapp/about/about.html',
            data : { pageTitle: 'About Us' }

        })

        .state('test', {
            url:'/test',
            templateUrl : 'static/templates/test.html',
            data : { pageTitle: 'test' },
            controller : 'testController',
            resolve: {
                imageri: function($http) {
                    var url = 'api/landing_page_images/';
                    return $http({ 
                        method: 'GET', 
                        url: url,
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
        })

        .state('services', {
            url:'/services',
            templateUrl : 'static/templates/userapp/services/services.html',
            data : { pageTitle: 'About Us' }

        })
        .state('contact', {
            url:'/contact',
            templateUrl : 'static/templates/userapp/contact/contact.html',
            isLogin: false,
            controller : 'contactUsController',
            data : { pageTitle: 'Hecms | Contact Us' }

        })
        .state('terms', {
            url:'/terms',
            templateUrl : 'static/templates/userapp/terms/terms.html',
            data : { pageTitle: 'Terms & Conditions' }

        })
        .state('inspections', {
            url:'/inspections',
            templateUrl : 'static/templates/userapp/inspections/inspections.html',
            isLogin: true,
            controller : 'inspectionsController',
            data : { pageTitle: 'Inspections' },
            resolve: {
                userProducts: function($http) {
                    user = JSON.parse(sessionStorage.getItem( 'userDataString'))
                    var url = 'api/auctionproducts/?lacks_service_type=Inspections'
                    return $http({ 
                        method: 'GET', 
                        url: url,
                    }).then(function(response){
                        console.log(JSON.stringify(response.data))
                        return response.data;
                    })
                },
                inspectionTypes: function($http) {
                    var url = 'api/inspectiontypes/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
        })

        .state('shipping', {
            url:'/shipping',
            templateUrl : 'static/templates/userapp/shipping/shipping.html',
            isLogin: true
        })
        .state('checkout_deposit', {
            url:'/checkout_deposit',
            templateUrl : 'static/templates/userapp/payments/checkout_deposit.html',
            isLogin: true,
            controller : 'bankDepositController',
            data : { pageTitle: 'Payments | Bank Deposit' },
            resolve: {
                bankAccounts: function($http) {
                    var url = 'api/bankaccounts/';
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(accounts){
                        console.log(JSON.stringify(accounts))
                        return accounts.data;
                    })
                }
            }
        })
        .state('payments1', {
            url:'/payments1',
            templateUrl : 'static/templates/userapp/payments/payments1.html',
            data : { pageTitle: 'Shopping Cart' },
            controller : 'shoppingCartController',
            isLogin: true,
            resolve: {
                shoppingCart: function($window) {
                    return JSON.parse($window.sessionStorage.getItem('shoppingCart'));
                }
            }

        })  

        .state('paymentmethod', {
            url:'/paymentmethod',
            templateUrl : 'static/templates/userapp/payments/paymentmethod.html',
            data : { pageTitle: 'Choose Payment Method' },
            controller : 'paymentMethodController',
            isLogin: true,
            resolve: {
                shoppingCart: function($window, $location) {
                    var shoppingCart = JSON.parse( $window.sessionStorage.getItem('shoppingCart') );
                    if( shoppingCart.length < 1 ){
                        $location.path( 'home' )
                    }else{
                       return shoppingCart; 
                    }
                    
                }
            }

        })  


        .state('paymenthistory', {
            url:'/paymenthistory',
            templateUrl : 'static/templates/userapp/paymenthistory/paymenthistory.html',
            isLogin: true,
            data : { pageTitle: 'Payment History' },
            controller : 'paymentHistoryController',
            resolve: {
                paymentHistory: function($http) {
                    var now_date = new Date()
                    var timestamp_lte = new Date();
                    var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
                    var url = 'api/payments/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString();
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                }
            }


        })

        .state('orderhistory', {
            url:'/orderhistory',
            templateUrl : 'static/templates/userapp/orderhistory/orderhistory.html',
            isLogin: true,
            data : { pageTitle: 'Auction Products' },
            controller : 'orderHistoryController'
        })

        .state('orderbook', {
            url:'/orderbook',
            templateUrl : 'static/templates/userapp/orderbook/orderbook.html',
            controller : 'orderBookController',
            data : { pageTitle: 'OrderBook' },
            isLogin: true,
            resolve: {
                OrderBook: function($http) {

                    var now_date = new Date()
                    var timestamp_lte = new Date();
                    var timestamp_gte = new Date(now_date.setDate( now_date.getDate() - 30 ))
                    var url = 'api/services/?timestamp_gte=' + timestamp_gte.toISOString() + '&timestamp_lte='+ timestamp_lte.toISOString();
                    return $http({ 
                        method: 'GET', 
                        url: url
                    }).then(function(response){
                        return response.data;
                    })
                },
                shoppingCart: function($window) {
                    return JSON.parse($window.sessionStorage.getItem('shoppingCart'));
                }
            }

        })

        .state('index', {
            url:'/',
            templateUrl : 'static/templates/userapp/index/index.html',
            controller : 'indexController',
            data : { pageTitle: 'Welcome' },
            isLogin: false,
            resolve: {
                gallery: function($http) {
                    var url = 'api/landing_page_images/';
                    return $http({ 
                        method: 'GET', 
                        url: url,
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
        })
        .state('profile', {
            url:'/profile',
            templateUrl : 'static/templates/userapp/profile/profile.html',
            controller : 'profileController',
            isLogin: true,
            data : { pageTitle: 'User Profile' },
            resolve: {
                sessionData: function($window) {
                    return JSON.parse($window.sessionStorage.getItem('userDataString'));

                }
            }
        })
        .state('maintenance', {
            url:'/maintenance',
            templateUrl : 'static/templates/userapp/maintenance/maintenance.html',
            controller : 'maintenanceController',
            data : { pageTitle: 'Maintenance' },
            isLogin: true,
            resolve: {
                userProducts: function($http) {
                    var url = 'api/auctionproducts/?lacks_service_type=Maintenance/';

                    return $http({ 
                        method: 'GET', 
                        url: url,
                    }).then(function(response){
                        return response.data;
                    })
                }
            }
            
        })

        .state('partsAccessories', {
            url:'/partsAccessories',
            templateUrl : 'static/templates/userapp/partsAccessories/partsAccessories.html',
            isLogin: true
        })

        .state('logistics', {
            url:'/logistics',
            templateUrl : 'static/templates/userapp/logistics/logistics.html',
            controller : 'logisticsController',
            data : { pageTitle: 'Logistics' },
            isLogin: true,
            resolve: {
                userProducts: function($http) {
                    var url = 'api/auctionproducts/?lacks_service_type=Logistics/';
                    return $http({ 
                        method: 'GET', 
                        url: url,
                    }).then(function(response){
                        return response.data;
                    })
                }
            }

        })

        .state('serviceRequestThanks', {
            url: '/serviceRequestThanks',
            templateUrl : 'static/templates/userapp/partials/serviceRequestThanks.html',
            controller: 'serviceRequestThanksController',
            isLogin: true
        })



        .state('home', {
            url: '/home',
            templateUrl : 'static/templates/userapp/home/home.html',
            controller: 'homePageController',
            data : { pageTitle: 'Hecms | Home' },
            isLogin: true,
            resolve: {
                auctions: function($http) {
                    var url = 'api/auctions/';
                    return $http({ 
                        method: 'GET', 
                        url: url,
                    }).then(function(response){
                        console.log(response.data)
                        return response.data;
                    })
                }
            }
        })

        .state('howitworks', {
            url: '/howitworks',
            templateUrl : 'static/templates/userapp/howitworks/howitworks.html',
            data : { pageTitle: 'How it works' }
        })

        .state('login', {
            //url:'/{oauth_token}login',
            url:'/login',
            data : { pageTitle: 'Hecms | Login' },
            templateUrl : 'static/templates/userapp/login/login.html',
            controller : 'signInController'

        })

        .state('join', {
            url: '/join',
            templateUrl : 'static/templates/userapp/join/join.html',
            controller : "joinController",
            data : { pageTitle: 'Hecms | Join' }
        })

        .state('forgot-password', {
            url:'/forgot-password',
            templateUrl : 'static/templates/userapp/forgotPassword/forgotPassword.html',
            controller : 'forgotPwdController',
            data : { pageTitle: 'Forgot Password' }

        })

        .state('help', {
            url:'/help',
            templateUrl : 'static/templates/userapp/help/help.html'

        })


        //  CAROUSEL ITEMS
        .state('inspection_carousel_detail', {
            url:'/inspection_carousel_detail',
            templateUrl : 'static/templates/userapp/carousel_detail/inspection_carousel_detail.html',
            data : { pageTitle: 'Hecms | Information' },
            controller : 'InspcarouselDetailController'

        })

        .state('sample_inspection_carousel_detail', {
            url:'/sample_inspection_carousel_detail',
            templateUrl : 'static/templates/userapp/sampleinspectionreport/sampleinspectionreport.html',
            data : { pageTitle: 'Hecms | Information' },
            controller : 'InspcarouselSampleDetailController'

        })



        .state('auction_carousel_detail', {
            url:'/auction_carousel_detail',
            templateUrl : 'static/templates/userapp/carousel_detail/auction_carousel_detail.html',
            isLogin: false,
            data : { pageTitle: 'Hecms | Information' },
            controller : 'auctionCarouselDetailController'

        })


        $urlRouterProvider.otherwise('/');
});


hmShipApp.config([
    '$httpProvider', function( $httpProvider ){
        $httpProvider.interceptors.push('tokenAuthInterceptor');
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
])

hmShipApp.config([
    '$interpolateProvider', function( $interpolateProvider ){
        $interpolateProvider.startSymbol('[[').endSymbol(']]'); 
    }
])



hmShipApp.run(['$rootScope', '$state', '$stateParams', '$location', 'userSessionServices', '$window', '$uibModal', 
    function($rootScope, $state, $stateParams, $location, userSessionServices, $window, $uibModal )
{



    //RUN CODE WHEN ROUTE CHANGES
    $rootScope.$on('$stateChangeStart', function(event, next, toStateParams){

        var authenticationStatus = userSessionServices.isAuthenticated();

        if(next.isLogin == undefined){

        }
        else if( !authenticationStatus && next.isLogin == true ){ // REDIRECT TO LOGIN IF ATTEMPTING TO ENTER AN AUTHENTICATED URL
            event.preventDefault()
            $rootScope.savedLocation = $location.url;
            $window.location.assign('/#login');;

        }else if(authenticationStatus && next.isLogin!= true  ){// NOT AN AUTHENTICATED URL WITH TOKEN AVAILABLE

            event.preventDefault();

            //IF NO USER DATA IS AVAILABLE GET IT

            if ($window.sessionStorage.getItem('userDataString')){
                $window.location.assign('/#home');
                //$location.path('#/home');
                // userSessionServices.userProfile().then(function( userInfo ){
                //     $location.path('home');
                // });    
            }


            $window.location.assign('/#home');

        }

        else if( next.isLogin == true && authenticationStatus  ){

            var userDataString = $window.sessionStorage.getItem( 'userDataString' )
            if (userDataString){
                var email = JSON.parse(userDataString).email;
                if (!email){
                    var modalInstance = $uibModal.open({
                        ariaLabelledBy: 'modal-title',
                        ariaDescribedBy: 'modal-body',
                        //animation: $scope.animationsEnabled,
                        templateUrl: '/static/templates/userapp/partials/requestEmail.html',
                        controller: 'requestEmailModalController',
                        size: 'md'
                    });      
                }
            }else{
                userSessionServices.userProfile().then(function( userInfo ){
                    $window.sessionStorage.setItem( 'userDataString', JSON.stringify(userInfo) )
                });   
            }



        }




        if( authenticationStatus == true){
            $rootScope.userAuthenticated = true;
            $rootScope.brandUrl = '#/home';
        }else{
            $rootScope.userAuthenticated = false;
            $rootScope.brandUrl = '#/';
        }

        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;


    });



}]);




// //JAVSCRIPT PROTOTYPE FUNCTIONS
Date.prototype.addDays = function(days) {
    this.setDate(this.getDate() + parseInt(days));
    return this;

};


Date.prototype.toISODate= function(){
    return String(this.getFullYear() + "-" + (this.getMonth() + 1) + "-" + 1);
}

Date.prototype.toUTC= function(){
var now_utc = new Date(this.getUTCFullYear(), this.getUTCMonth(), this.getUTCDate(),  this.getUTCHours(), this.getUTCMinutes(), this.getUTCSeconds());
    return now_utc;
}




Date.prototype.monthDays= function(){
    var d= new Date(this.getUTCFullYear(), this.getMonth()+1, 0);
    return d.getDate();
}

