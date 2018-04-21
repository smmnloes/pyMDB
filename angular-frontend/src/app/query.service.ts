import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {SearchModel} from "./content/search-page/search-form/search-model";
import {Subject} from "rxjs/Subject";
import {resultModel} from "./content/search-page/search-results/result/resultModel";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable()
export class QueryService {

  private resultsSource = new Subject<resultModel[]>();
  results$ = this.resultsSource.asObservable();

  private newQuerySource = new Subject<boolean>();
  newQuery$ = this.newQuerySource.asObservable();

  resultCountSource = new Subject<number>();
  resultCount$ = this.resultCountSource.asObservable();

  lastQuery: SearchModel = null;

  PAGE_SIZE = 15;

  resultCache: resultModel[][] = [];

  constructor(private http: HttpClient) {
  }


  makeQuery(queryData: SearchModel, isNewQuery: boolean) {
    if (isNewQuery) {
      this.resultCache = [];
    } else {
      let storedResult = this.resultCache[queryData.currentPage];
      if (storedResult != null) {
        console.log('returning stored data!');
        this.resultsSource.next(storedResult);
        return;
      }
    }

    queryData.page_size = this.PAGE_SIZE;
    this.lastQuery = queryData.clone();

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        let processedResult: resultModel[] = QueryService.processResult(data);
        this.resultsSource.next(processedResult);

        if (this.resultCache[queryData.currentPage] == null) {
          console.log('writing new data to array');
          this.resultCache[queryData.currentPage] = processedResult;
        }

        console.log(this.resultCache);

        this.newQuerySource.next(isNewQuery);
      }
    );

    if (isNewQuery) {
      this.http.post('api/result_count', queryData, httpOptions).subscribe(resultCount => {

        this.resultCountSource.next(<number>resultCount);
      })
    }

  }

  static processResult(data): resultModel[] {
    let results: resultModel[] = [];
    for (let result of data) {
      results.push(new resultModel(
        result.averageRating,
        result.directors,
        result.genres,
        result.primaryTitle,
        result.principals,
        result.runtimeMinutes,
        result.tid,
        result.year
      ));

    }
    return results;
  }

  loadPage(page: number) {
    this.lastQuery.currentPage = page;
    this.makeQuery(this.lastQuery, false);
  }


}

