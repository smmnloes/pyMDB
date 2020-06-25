import {HttpHeaders} from "@angular/common/http";

export class Util {
  public static isEmpty(object: Object): boolean {
    return Object.getOwnPropertyNames(object).length === 0;
  }

  public static appJsonHeaderOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  };

}
