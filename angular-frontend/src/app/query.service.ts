import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {SearchModel} from "./content/search-page/search-form/search-model";
import {Subject} from "rxjs/Subject";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable()
export class QueryService {

  private resultsSource = new Subject<any[]>();
  results$ = this.resultsSource.asObservable();

  private newQuerySource = new Subject<boolean>()
  newQuery$ = this.newQuerySource.asObservable();

  resultCountSource = new Subject<number>();
  resultCount$ = this.resultCountSource.asObservable();

  lastQuery: SearchModel = null;

  PAGE_SIZE = 20;


  constructor(private http: HttpClient) {
  }


  makeQuery(queryData: SearchModel, isNewQuery: boolean) {
    queryData.page_size = this.PAGE_SIZE;
    this.lastQuery = queryData.clone();

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        this.resultsSource.next(<any[]>data);
        this.newQuerySource.next(isNewQuery);
      }
    );

    if (isNewQuery) {
      this.http.post('api/result_count', queryData, httpOptions).subscribe(resultCount => {
        this.resultCountSource.next(<number>resultCount);
        console.log(resultCount)
      })
    }


  }

  loadPage(page: number) {
    this.lastQuery.currentPage = page;
    this.makeQuery(this.lastQuery, false);
  }


}

