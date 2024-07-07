## KegWatch API Documentation


------------------------------------------------------------------------------------------



#### Keg Management

<details>
 <summary><code>GET</code> <code><b>/kegs/all</b></code> <code>(gets all kegs and attributes)</code></summary>
</details>

<details>
 <summary><code>GET</code> <code><b>/kegs/active</b></code> <code>(gets all active kegs and attributes)</code></summary>
</details>

<details>
 <summary><code>GET</code> <code><b>/kegs/active?tap={tap_id}</b></code> <code>(gets active keg and attributes from a specific tap)</code></summary>
</details>

<details>
  <summary><code>POST</code> <code><b>/kegs/create</b></code> <code>(creates a new keg)</code></summary>

##### Parameters

> | name   |  type      | data type      | description                                          |
> |--------|------------|----------------|------------------------------------------------------|
> | `name` |  required  | string         | The name of the beer                  |
> | `tap` |  required  | int         | The tap number it is being connected to                 |
> | `abv` |  required  | float         | The ABV for the beer                  |
> | `capacity` |  required  | float         | Capacity in oz of the keg                 |
> | `date_tapped` |  required  | datetime         | The date it was tapped (YYYY-MM-DD)                 |

</details>

<details>
  <summary><code>POST</code> <code><b>/kegs/kick</b></code> <code>(marks an existing keg as kicked)</code></summary>

##### Parameters

> | name   |  type      | data type      | description                                          |
> |--------|------------|----------------|------------------------------------------------------|
> | `keg_id` |  required  | string         | The UUID of the keg                 |

</details>



------------------------------------------------------------------------------------------



#### User Management

<details>
 <summary><code>GET</code> <code><b>/users/list</b></code> <code>(gets all users and attributes)</code></summary>
</details>

<details>
  <summary><code>POST</code> <code><b>/users/remove</b></code> <code>(deletes a user)</code></summary>

##### Parameters

> | name   |  type      | data type      | description                                          |
> |--------|------------|----------------|------------------------------------------------------|
> | `user_id` |  required  | string         | The UUID of the user                 |

</details>

<details>
  <summary><code>POST</code> <code><b>/users/create</b></code> <code>(creates a user)</code></summary>

##### Parameters

> | name   |  type      | data type      | description                                          |
> |--------|------------|----------------|------------------------------------------------------|
> | `name` |  required  | string         | The name (First Last) of the user                 |
> | `weight` |  required  | float         | The weight of the user in grams                 |
> | `gender` |  required  | int         | The gender of the user (0 = Male, 1 = Female)                |

</details>

<details>
  <summary><code>POST</code> <code><b>/users/modify</b></code> <code>(modifies the properties of an existing user)</code></summary>

##### Parameters

> | name   |  type      | data type      | description                                          |
> |--------|------------|----------------|------------------------------------------------------|
> | `user_id` |  required  | string         | The UUID of the user                 |
> | `name` |  required  | string         | The name (First Last) of the user                 |
> | `weight` |  required  | float         | The weight of the user in grams                 |
> | `gender` |  required  | int         | The gender of the user (0 = Male, 1 = Female)                |

</details>

<details>
 <summary><code>GET</code> <code><b>/pass/user?consumer={first+last}</b></code> <code>(gets the total oz poured and favorite beer of the user)</code></summary>
</details>


------------------------------------------------------------------------------------------


#### Beer Management
<details>
  <summary><code>POST</code> <code><b>/beer/pour</b></code> <code>(logs a pour of beer)</code></summary>

##### Parameters

> | name   |  type      | data type      | description                                          |
> |--------|------------|----------------|------------------------------------------------------|
> | `tap_id` |  required  | int         | The ID for the tap                  |
> | `keg_id` |  required  | string         | The UUID of the keg                 |
> | `consumer` |  required  | string         | The user's First and Last name                  |
> | `oz_poured` |  required  | float         | The amount poured in oz                |

</details>

------------------------------------------------------------------------------------------


