import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {SearchModel} from "./content/search-page/search-form/search-model";
import {Subject} from "rxjs/Subject";
import {ResultModel} from "./content/search-page/search-results/result/result-model";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable()
export class QueryService {

  private resultsSource = new Subject<ResultModel[]>();
  results$ = this.resultsSource.asObservable();

  resultCountSource = new Subject<number>();
  resultCount$ = this.resultCountSource.asObservable();

  lastQuery: SearchModel = null;

  PAGE_SIZE = 15;

  cachedPages: ResultModel[][] = [];

  constructor(private http: HttpClient) {
  }


  makeQuery(queryData: SearchModel, isNewQuery: boolean) {

    // Clear page cache if query is new,
    // else return cached page if available
    if (isNewQuery) {
      this.cachedPages = [];
    } else {
      let cachedResult = this.cachedPages[queryData.current_page];
      if (cachedResult != null) {
        this.resultsSource.next(cachedResult);
        return;
      }
    }

    queryData.page_size = this.PAGE_SIZE;
    this.lastQuery = queryData.clone();

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        let processedResult: ResultModel[] = QueryService.processResult(data);
        this.resultsSource.next(processedResult);

        if (this.cachedPages[queryData.current_page] == null) {
          this.cachedPages[queryData.current_page] = processedResult;
        }

      }
    );

    // get new result count if query is new
    if (isNewQuery) {
      this.http.post('api/result_count', queryData, httpOptions).subscribe(resultCount => {
        this.resultCountSource.next(<number>resultCount);
      })
    }

  }

  static processResult(data): ResultModel[] {
    let results: ResultModel[] = [];
    for (let result of data) {
      results.push(new ResultModel(
        result.average_rating,
        result.directors,
        result.genres,
        result.primary_title,
        result.principals,
        result.runtime_minutes,
        result.tid,
        result.year
      ));

    }
    return results;
  }

  loadPage(page: number) {
    this.lastQuery.current_page = page;
    this.makeQuery(this.lastQuery, false);
  }

  changeSortBy(criteria: string) {
    this.lastQuery.sort_by = criteria;
    this.makeQuery(this.lastQuery, true);
  }


}

