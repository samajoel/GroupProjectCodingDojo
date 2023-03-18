var data = {
    "orders": [
      {
        "orderno": 784692,
        "date": "June 30, 2088 1:54:23 AM",
        "trackingno": "TN000391",
        "customer": {
          "custid": 11045,
          "fname": "Sue",
          "lname": "Hatfield",
          "address": "1409 Silver Street",
          "city": "Ashland",
          "state": "NE",
          "zip": 68003
        }
      },
      {
        "orderno": 784693,
        "date": "March 3, 2088 8:18:14 PM",
        "trackingno": "TN000468",
        "customer": {
          "custid": 11045,
          "fname": "Sue",
          "lname": "Hatfield",
          "address": "1409 Silver Street",
          "city": "Ashland",
          "state": "NE",
          "zip": 68003
        }
      }
    ]
  }
  

  
  console.log(typeof(data));
  // 'object'
  console.log(Array.isArray(data));
  // false
  console.log(Array.isArray(data.orders));
  // true
  