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
      let cachedResult = this.cachedPages[queryData.currentPage];
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

        if (this.cachedPages[queryData.currentPage] == null) {
          this.cachedPages[queryData.currentPage] = processedResult;
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

  changeSortBy(criteria: string) {
    this.lastQuery.sortBy = criteria;
    this.makeQuery(this.lastQuery, true);
  }


}

