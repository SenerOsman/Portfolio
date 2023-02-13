const EXAMPLE_CATEGORY = {
    name: randomString()
}

const EXAMPLE_CATEGORIES = {
    categories: [
        EXAMPLE_CATEGORY
    ]
}

const PRICE = Math.floor(Math.random() * 100) * 100;

const EXAMPLE_PRODUCT = {
    title: 'zzzzz product',
    description: randomString(64),
    thumbnail: 'thumbnail url',
    image: 'image url',
    price: PRICE,
    price_vat: PRICE * 1.21,
    stock: 23,
    category: EXAMPLE_CATEGORY
}

const EXAMPLE_PRODUCTS = {
    products: [
        EXAMPLE_PRODUCT
    ]
}

const EXAMPLE_COUNTRY = {
    name: 'Netherlands'
}

const EXAMPLE_COUNTRIES = {
    countries: [
        EXAMPLE_COUNTRY
    ]
}

const EXAMPLE_USERROLE = {
    name: 'customer'
}

const EXAMPLE_USER = {
    username: 'test_user',
    email: randomString(7) + '@windesheim.nl',
    newsletter: 0,
    userrole: EXAMPLE_USERROLE,
    country: EXAMPLE_COUNTRY
}

const EXAMPLE_USERS = {
    users: [
        EXAMPLE_USER
    ]
}

const EXAMPLE_ORDER = {
    date: 0,
    payed: 0,
    user: EXAMPLE_USER,
    order_regs: [{
        id: 2,
        product: 0,
        order: 1,
        amount: 1,
        total_price: 19995
    }]
}

/**
 * Test GET request on /products
 */
function testGetProducts(event) {
    testApiGET('products', EXAMPLE_PRODUCTS, 'title');
}

/**
 * Test GET request on /products/1
 */
function testGetProduct() {
    testApiGET('products/1', EXAMPLE_PRODUCT);
}

/**
 * Test POST request on /products
 */
function testPostProduct() {
    let product = { ...EXAMPLE_PRODUCT }
    delete product.price_vat;
    testApiPOST('products', product, true);
}

/**
 * Test PATCH request on /products
 */
function testPatchProduct() {
    testApiPATCH('products', EXAMPLE_PRODUCT, {
        title: randomString()
    });
}

/**
 * Test DELETE request on /products
 */
function testDeleteProduct() {
    testApiDELETE('products', EXAMPLE_PRODUCT);
}

/**
 * Test GET request on /categories
 */
function testGetCategories() {
    testApiGET('categories', EXAMPLE_CATEGORIES);
}

/**
 * Test GET request on /categories/1
 */
function testGetCategory() {
    testApiGET('categories/1', EXAMPLE_CATEGORY);
}

/**
 * Test POST request on /categories
 */
function testPostCategory() {
    testApiPOST('categories', EXAMPLE_CATEGORY, true);
}

/**
 * Test GET request on /categories/1/products
 */
function testGetCategoryproducts() {
    testApiGET('categories/1/products', EXAMPLE_PRODUCTS);
}

/**
 * Test GET request on /users
 */
function testGetUsers() {
    testApiGET('users', EXAMPLE_USERS);
}

/**
 * Test GET request on /users/1
 */
function testGetUser() {
    testApiGET('users/1', EXAMPLE_USER);
}

/**
 * Test POST request on /users
 */
function testPostUser() {
    var user = {
        ...EXAMPLE_USER
    };
    user.password = 'welcome123';
    testApiPOST('users', user);
}

/**
 * Test PATCH request on /users
 */
function testPatchUser() {
    var user = {
        ...EXAMPLE_USER
    };
    user.password = 'welcome123';
    testApiPATCH('users', user, {
        newsletter: 1
    });
}

/**
 * Test DELETE request on /users
 */
function testDeleteUser() {
    var user = {
        ...EXAMPLE_USER
    };
    user.password = 'welcome123';
    testApiDELETE('users', user);
}



// variable needed to query a deleted resource and see if it is in fact, deleted
var deleteId;

/**
 * 
 * @param {object} response 
 * @param {string} status 
 */
function defaultFailedCallback(response, status) {
    console.error('test failed. Server responded with status: ' + status);
    notify('test failed. Server responded with status: ' + status, 'error');
}

function testFailed(message) {
    notify(message, 'error');
}

function testSuccess(message) {
    notify(message, 'info');
}

function notify(msg, type) {
    let n = document.createElement("div");
    n.innerText = msg;
    n.className = type;
    $('#notifications').appendChild(n);
    setTimeout(function () {
        n.parentElement.removeChild(n);
    }, 10000);
}

/**
 * 
 * @param {string} url 
 * @param {object} object 
 */
function testApiDELETE(url, object) {
    for (let key in object) {
        if (typeof (object[key]) == 'object') {
            object[key] = 1;
        }
    }
    // create
    api(
        url,
        (response, status) => {
            // get
            api(
                url,
                (response, status) => {
                    // delete
                    deleteId = response[url][response[url].length - 1].id
                    api(
                        url + '/' + deleteId,
                        (response, status) => {
                            // get (this one should fail)
                            api(
                                url + '/' + deleteId,
                                defaultFailedCallback,
                                (response, status) => {
                                    if (status == 404) {
                                        testSuccess('DELETE successful');
                                    } else {
                                        testFailed('Querying deleted product did not result in 404 but in ' + status);

                                    }
                                }
                            )
                        },
                        defaultFailedCallback,
                        'DELETE'
                    )
                },
                defaultFailedCallback
            )
        },
        defaultFailedCallback,
        'POST',
        object
    )
}

/**
 * 
 * @param {string} url 
 * @param {object} object 
 * @param {object} change 
 */
function testApiPATCH(url, object, change) {
    for (let key in object) {
        if (typeof (object[key]) == 'object') {
            object[key] = 1;
        }
    }
    // create
    api(
        url,
        (response, status) => {
            // get
            api(
                url,
                (response, status) => {
                    // change
                    api(
                        url + '/' + response[url][response[url].length - 1].id,
                        (response, status) => {
                            try {
                                compareObjects(change, response);
                                testSuccess('PATCH successful');
                            } catch (err) {
                                testFailed(err);
                            }
                        },
                        defaultFailedCallback,
                        'PATCH',
                        change
                    )
                },
                defaultFailedCallback
            )
        },
        defaultFailedCallback,
        'POST',
        object
    )
}

/**
 * 
 * @param {string} url 
 * @param {object} object 
 * @param {boolean} convert_foreign_keys 
 */
function testApiPOST(url, object, convert_foreign_keys = true) {
    if (convert_foreign_keys) {
        for (let key in object) {
            if (typeof (object[key]) == 'object') {
                object[key] = 1;
            }
        }
    }
    api(
        url,
        (response, status) => {
            api(
                url,
                (response, status) => {
                    obj = response[url][response[url].length - 1];
                    try {
                        compareObjects(object, obj);
                        testSuccess('POST successful');
                    } catch (err) {
                        testFailed(err);
                    }
                },
                defaultFailedCallback
            )
        },
        defaultFailedCallback,
        'POST',
        object
    )
}

/**
 * 
 * @param {string} url 
 * @param {object} responseStructure 
 * @param {string} alphabetical The name of the alphabetical column
 */
function testApiGET(url, responseStructure, alphabetical = '') {
    api(
        url,
        (response, status) => {
            try {
                compareStructure(response, responseStructure, 'response');
                if (alphabetical) {
                    for (let key in response) {
                        let alph = '0';
                        for (let i in response[key]) {
                            if (alph < response[key][i][alphabetical]) {
                                alph = response[key][i][alphabetical];
                            } else {
                                throw new Error('column ' + alphabetical + ' is not in alphabetical order!');
                            }
                        }
                    }
                }
                testSuccess('GET successful');
            } catch (err) {
                testFailed(err);
            }

        },
        defaultFailedCallback
    )
}

/**
 * 
 * @param {object} template 
 * @param {object} object 
 */
function compareObjects(template, object) {
    for (let key in template) {
        if (key == 'password') continue;
        if (typeof (object[key]) == 'object') {
            if (template[key] != object[key].id) {
                throw new Error('relation to ' + key + ' is not saved correctly. is id \'' + object[key].id + '\' but should be id \'' + template[key] + '\'');
            }
        } else {
            if (template[key] != object[key]) {
                throw new Error('key ' + key + ' is not saved correctly. is \'' + object[key] + '\' but should be \'' + template[key] + '\'');
            }
        }
    }
}

/**
 * 
 * @param {object} object 
 * @param {object} structure 
 * @param {string} objectname 
 */
function compareStructure(object, structure, objectname = '') {
    for (let key in structure) {
        testKey(key, object, objectname);
        if (typeof (structure[key]) == 'object') {
            compareStructure(object[key], structure[key], objectname + (isNaN(key) ? '.' + key : '[' + key + ']'));
        }
    }
}

/**
 *  
 * @param {array} keys 
 * @param {object} obj 
 */
function testKeys(keys, obj) {
    for (let i = 0; i < keys.length; i++) {
        let key = keys[i];
        testKey(key, obj);
    }
}

/**
 * 
 * @param {string} key 
 * @param {object} obj 
 * @param {string} objectName 
 */
function testKey(key, obj, objectName = 'object') {
    if (!(key in obj)) {
        throw new Error('no ' + key + ' found in ' + objectName);
    }
}

/**
 * 
 * @param {number} length 
 */
function randomString(length = 16) {
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let str = '';
    for (let i = 0; i < length; i++) {
        str += characters.charAt(Math.floor(Math.random() * length));
    }
    return str;
}