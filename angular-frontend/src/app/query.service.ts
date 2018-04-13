import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable()
export class QueryService {

  constructor(private http: HttpClient) {
  }

  makeQuery(queryData) {
    return this.http.post('api/query', queryData, httpOptions);
  }

}
