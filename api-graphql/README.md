# GRAPHQL-API

## DBModel
![](/home/gonzalo/dev/rcn-api/dbmodel.png)

## Querys

Las siguientes querys estan disponibles

* modeldebtinfo
* debt
* config
* state
* loan
* commit

### modeldebtinfo

#### Query
```json
{
  modeldebtinfo(id:"0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca") {
    paid
    due_time
    estimated_obligation
    next_obligation
    current_obligation
    debt_balance
    owner
  }
}
```

#### Response 
```json
{
  "data": {
    "modeldebtinfo": {
      "paid": "3000000000000000000",
      "due_time": "1568322487",
      "estimated_obligation": "9000000000000000000",
      "next_obligation": "1000000000000000000",
      "current_obligation": "0",
      "debt_balance": "3000000000000000000",
      "owner": "0xA3e8218618762A249EC75BD923F1b299945664C3"
    }
  },
  "errors": null
}
```
#### Parameters

| Name | Type | Required | Example |
|------|------|----------|---------|
| id | String | True | "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca" |


#### Fields

| Name | Type |
|------|------|
| paid | String |
| due_time | String |
| estimated_obligation | String |
| next_obligation | String |
| current_obligation | String |
| debt_balance | String |
| owner | String |

### Debt

#### Query

```json
{
  debt {
    id
    error
    balance
    model
    creator
    oracle
    created
    modeldebtinfo {
      paid
      due_time
      estimated_obligation
      next_obligation
      current_obligation
      debt_balance
      owner
    }
  }
}
```

#### Response

```json
{
  "data": {
    "debt": [
      {
        "id": "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca",
        "error": false,
        "balance": "3000000000000000000",
        "model": "0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF",
        "creator": "0xC78A11c729275E656fa3decc1f15aeBEe69d08FC",
        "oracle": "0x0000000000000000000000000000000000000000",
        "created": "1557954487",
        "modeldebtinfo": {
          "paid": "3000000000000000000",
          "due_time": "1568322487",
          "estimated_obligation": "9000000000000000000",
          "next_obligation": "1000000000000000000",
          "current_obligation": "0",
          "debt_balance": "3000000000000000000",
          "owner": "0xA3e8218618762A249EC75BD923F1b299945664C3"
        }
      },
      {
        "id": "0x3dab750ff04c67326e63914703423ed192befbd1b3d52d84c72663f6ce7c05a4",
        "error": false,
        "balance": "0",
        "model": "0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF",
        "creator": "0xC78A11c729275E656fa3decc1f15aeBEe69d08FC",
        "oracle": "0xd8320C70F5D5B355e1365acdF1F7C6fE4D0d92Cf",
        "created": "1558541051",
        "modeldebtinfo": {
          "paid": "0",
          "due_time": "1584461051",
          "estimated_obligation": "1400",
          "next_obligation": "140",
          "current_obligation": "0",
          "debt_balance": "0",
          "owner": "0x6684C2F982758685780b8d488c32fAfA4d008A53"
        }
      }
    ]
  },
  "errors": null
}
```

#### Parameters

| Name | Type | Required | Example |
|------|------|----------|---------|
| id | String | False | "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca" |
| error | Boolean | False | false |
| model | String | False | "0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF" |
| creator | String | False | "0xC78A11c729275E656fa3decc1f15aeBEe69d08FC" |
| oracle | String | False | "0x0000000000000000000000000000000000000000" |
| balance__gt | String | False | "12345" |
| balance__gte | String | False | "12345" |
| balance__lt | String | False | "12345" |
| balance__lte | String | False | "12345" |
| created__gt | String | False | "12345" |
| created__gt | String | False | "12345" |
| created__gt | String | False | "12345" |
| created__gt | String | False | "12345" |
| first | Integer | False | 1 |
| skip | Integer | False | 4 |



#### Fields

| Name | Type |
|------|------|
| id | String |
| error | Boolean |
| balance | String |
| model | String |
| creator | String |
| oracle | String |
| created | String |
| modeldebtinfo | ModelDebtInfo |


## Config

#### Query

```json
{
  config {
    id
    data
  }
}
```


#### Response

```json
{
  "data": {
    "config": [
      {
        "id": "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca",
        "data": "{\"installments\": \"12\", \"time_unit\": \"2\", \"duration\": \"2592000\", \"lent_time\": \"1557954487\", \"cuota\": \"1000000000000000000\", \"interest_rate\": \"25970000000000\"}"
      },
      {
        "id": "0x3dab750ff04c67326e63914703423ed192befbd1b3d52d84c72663f6ce7c05a4",
        "data": "{\"installments\": \"10\", \"time_unit\": \"2592000\", \"duration\": \"25920000\", \"lent_time\": \"1558541051\", \"cuota\": \"140\", \"interest_rate\": \"1295979264000\"}"
      }
    ]
  },
  "errors": null
}
```

#### Parameters

| Name | Type | Required | Example |
|------|------|----------|---------|
| id | String | False | "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca" |


#### Fields

| Name | Type |
|------|------|
| id | String |
| data | JSONString |

### State

#### Query

```json
{
  state {
    id
    status
    clock
    lastPayment
    paid
    paidBase
    interest
  }
}
```


### Response

```json
{
  "data": {
    "state": [
      {
        "id": "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca",
        "status": "0",
        "clock": "10368000",
        "lastPayment": "10368000",
        "paid": "3000000000000000000",
        "paidBase": "3000000000000000000",
        "interest": "0"
      },
      {
        "id": "0x3dab750ff04c67326e63914703423ed192befbd1b3d52d84c72663f6ce7c05a4",
        "status": "0",
        "clock": "25920000",
        "lastPayment": "0",
        "paid": "0",
        "paidBase": "0",
        "interest": "0"
      }
    ]
  },
  "errors": null
}
```

#### Parameters

| Name | Type | Required | Example |
|------|------|----------|---------|
| id | String | False | "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca" |
| status | String | False | "0" |
| first | Integer | False | 1 |
| skip | Integer | False | 2 |


#### Fields

| Name | Type |
|------|------|
| id | String |
| status | String |
| clock | String |
| lastPayment | String |
| paid | String |
| paidBase | String |
| interest | String |


### Loan

#### Query

```json
{
  loan {
    id
    open
    approved
    expiration
    amount
    cosigner
    model
    creator
    oracle
    borrower
    loanData
    created
    descriptor {
      firstObligation
      totalObligation
      duration
      interestRate
      punitiveInterestRate
      frequency
      installments
    }
    currency
    status
    canceled
    lender
    
  }
}
```

#### Response

```json
{
  "data": {
    "loan": [
      {
        "id": "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca",
        "open": false,
        "approved": true,
        "expiration": "1577953062",
        "amount": "11900000000000000000",
        "cosigner": "0x0000000000000000000000000000000000000000",
        "model": "0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF",
        "creator": "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C",
        "oracle": "0x0000000000000000000000000000000000000000",
        "borrower": "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C",
        "loanData": "0x00000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000000179e9c9ff40000000c0000278d0000000002",
        "created": "1557953102",
        "descriptor": {
          "firstObligation": "1000000000000000000",
          "totalObligation": "12000000000000000000",
          "duration": "31104000",
          "interestRate": "0.8364456893868629",
          "punitiveInterestRate": "25970000000000",
          "frequency": "2592000",
          "installments": "12"
        },
        "currency": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "status": "1",
        "canceled": false,
        "lender": "0xA3e8218618762A249EC75BD923F1b299945664C3"
      },
      {
        "id": "0x212c362e33abf6e3e6354363e0634aa1300c3045a18c8c5a08f3bb2a17184768",
        "open": true,
        "approved": true,
        "expiration": "1677953062",
        "amount": "11000000000000000000",
        "cosigner": "0x0000000000000000000000000000000000000000",
        "model": "0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF",
        "creator": "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C",
        "oracle": "0x0000000000000000000000000000000000000000",
        "borrower": "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C",
        "loanData": "0x00000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000000179e9c9ff40000000c0000278d0000000002",
        "created": "1557953119",
        "descriptor": {
          "firstObligation": "1000000000000000000",
          "totalObligation": "12000000000000000000",
          "duration": "31104000",
          "interestRate": "9.048821548821541",
          "punitiveInterestRate": "25970000000000",
          "frequency": "2592000",
          "installments": "12"
        },
        "currency": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "status": "0",
        "canceled": false,
        "lender": null
      }
    ]
  },
  "errors": null
}
```
#### Parameters

| Name | Type | Required | Example |
|------|------|----------|---------|
| id | String | False | "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca" |
| open | Boolean | False | false |
| approved | Boolean | False | false |
| cosigner | String | False | 0x0000000000000000000000000000000000000000 |
| model | String | False | "0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF" |
| creator | String | False | "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C" |
| oracle | String | False | "0x0000000000000000000000000000000000000000" |
| borrower | String | False | "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C" |
| currency | String | False | "0x0000000000000000000000000000000000000000000000000000000000000000" |
| status | String | False | "1" |
| canceled | Boolean | False | false |
| lender | String | False | "0xA3e8218618762A249EC75BD923F1b299945664C3" |
| expiration__gt | String | False | "1234" |
| expiration__gte | String | False | "1234" |
| expiration__lt | String | False | "1234" |
| expiration__lte | String | False | "1234" |
| amount__gt | String | False | "1234" |
| amount__gte | String | False | "1234" |
| amount__lt | String | False | "1234" |
| amount__lte | String | False | "1234" |
| created__gt | String | False | "1234" |
| created__gte | String | False | "1234" |
| created__lt | String | False | "1234" |
| created__lte | String | False | "1234" |
| first | Integer | False | 1 |
| skip | Integer | False | 2 |


#### Fields

#### Loan

| Name | Type |
|------|------|
| id | String |
| open | Boolean |
| approved | Boolean |
| expiration | String |
| amount | String |
| cosigner | String |
| model | String |
| creator | String |
| oracle | String |
| borrower | String |
| loanData | String |
| created | String |
| descriptor | Descriptor |
| currency | String |
| status | String |
| canceled | String |
| lender | String |

#### Descriptor

| name | type |
|------|------|
| firstObligation | String |
| totalObligation | String |
| duration | String |
| interestRate | String |
| punitiveInterestRate | String |
| frequency | String |
| installments | String |


### Commit

#### Query

```json
{
  commit {
    idLoan
    opcode
    timestamp
    order
    proof
    data
    address
  }
}
```

#### Response

```json
{
  "data": {
    "commit": [
      {
        "idLoan": "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca",
        "opcode": "requested_loan_manager",
        "timestamp": 1557953102,
        "order": 0,
        "proof": "0x49678a515109e837f31440c1e85db08e044d084e9c5e612f2d102174961d7290",
        "data": "{\"id\": \"0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca\", \"open\": true, \"approved\": true, \"position\": \"0\", \"expiration\": \"1577953062\", \"amount\": \"11900000000000000000\", \"cosigner\": \"0x0000000000000000000000000000000000000000\", \"model\": \"0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF\", \"creator\": \"0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C\", \"oracle\": \"0x0000000000000000000000000000000000000000\", \"borrower\": \"0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C\", \"salt\": \"1\", \"loanData\": \"0x00000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000000179e9c9ff40000000c0000278d0000000002\", \"created\": \"1557953102\", \"currency\": \"0x0000000000000000000000000000000000000000000000000000000000000000\", \"status\": \"0\", \"descriptor\": {\"first_obligation\": \"1000000000000000000\", \"total_obligation\": \"12000000000000000000\", \"duration\": \"31104000\", \"interest_rate\": \"0.8364456893868629\", \"punitive_interest_rate\": \"25970000000000\", \"frequency\": \"2592000\", \"installments\": \"12\"}}",
        "address": "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C"
      },
      {
        "idLoan": "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca",
        "opcode": "approved_loan_manager",
        "timestamp": 1557953102,
        "order": 1,
        "proof": "0x49678a515109e837f31440c1e85db08e044d084e9c5e612f2d102174961d7290",
        "data": "{\"id\": \"0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca\", \"approved\": true}",
        "address": "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C"
      },
      {
        "idLoan": "0x212c362e33abf6e3e6354363e0634aa1300c3045a18c8c5a08f3bb2a17184768",
        "opcode": "requested_loan_manager",
        "timestamp": 1557953119,
        "order": 2,
        "proof": "0xf6c088ac5373e9c560ee98875855a9c4bf7753f3a1e17eca5db825b06503b959",
        "data": "{\"id\": \"0x212c362e33abf6e3e6354363e0634aa1300c3045a18c8c5a08f3bb2a17184768\", \"open\": true, \"approved\": true, \"position\": \"0\", \"expiration\": \"1677953062\", \"amount\": \"11000000000000000000\", \"cosigner\": \"0x0000000000000000000000000000000000000000\", \"model\": \"0x97d0300281C55DC6BE27Cf57343184Ab5C8dcdFF\", \"creator\": \"0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C\", \"oracle\": \"0x0000000000000000000000000000000000000000\", \"borrower\": \"0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C\", \"salt\": \"2\", \"loanData\": \"0x00000000000000000de0b6b3a76400000000000000000000000000000000000000000000000000000000179e9c9ff40000000c0000278d0000000002\", \"created\": \"1557953119\", \"currency\": \"0x0000000000000000000000000000000000000000000000000000000000000000\", \"status\": \"0\", \"descriptor\": {\"first_obligation\": \"1000000000000000000\", \"total_obligation\": \"12000000000000000000\", \"duration\": \"31104000\", \"interest_rate\": \"9.048821548821541\", \"punitive_interest_rate\": \"25970000000000\", \"frequency\": \"2592000\", \"installments\": \"12\"}}",
        "address": "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C"
      }
    ]
  },
  "errors": null
}
```

#### Parameters

| Name | Type | Required | Example |
|------|------|----------|---------|
| idLoan | String | False | "0xfb7eafb131ec831df9a8f6255d4be4e86b079900c72f5baadb39336cbde199ca" |
| opcode | String | False | "lent_loan_manager" |
| proof | String | False | "lent_loan_manager" |
| address | String | False | "lent_loan_manager" |
| first | Integer | False | 1 |
| skip | Integer | False | 2 |


#### Fields

| Name | Type | 
|------|------|
| idLoan | String |
| opcode | String |
| timestamp | Integer |
| order | Integer |
| proof | String |
| data | JSONString |
| address | String |






