import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {BasicDataModel} from "./header/content/search-page/search-results/result/basic-data-model";
import {QueryModel} from "./header/content/search-page/search-form/query-model";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable()
export class QueryService {

  private basicDataSource = new Subject<BasicDataModel[]>();
  basicData$ = this.basicDataSource.asObservable();

  resultCountSource = new Subject<number>();
  resultCount$ = this.resultCountSource.asObservable();

  lastQuery: QueryModel = null;

  RESULTS_PER_PAGE = 15;

  cachedPages: BasicDataModel[][] = [];

  constructor(private http: HttpClient) {
  }


  makeQuery(queryData: QueryModel, isNewQuery: boolean) {

    // Clear page cache if query is new,
    // else return cached page if available
    if (isNewQuery) {
      this.cachedPages = [];
    } else {
      let cachedPage = this.cachedPages[queryData.current_page];
      if (cachedPage != null) {
        this.basicDataSource.next(cachedPage);
        return;
      }
    }

    queryData.results_per_page = this.RESULTS_PER_PAGE;
    this.lastQuery = queryData.clone();

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        let processedResult: BasicDataModel[] = QueryService.processBasicData(data);
        this.basicDataSource.next(processedResult);

        if (this.cachedPages[queryData.current_page] == null) {
          this.cachedPages[queryData.current_page] = processedResult;
        }

      }
    );

    if (isNewQuery) {
      this.getResultCount(queryData);
    }

  }

  private getResultCount(queryData: QueryModel) {
    this.http.post('api/result_count', queryData, httpOptions).subscribe(resultCount => {
      this.resultCountSource.next(<number>resultCount);
    })
  }

  static processBasicData(basicData): BasicDataModel[] {
    let results: BasicDataModel[] = [];
    for (let result of basicData) {
      results.push(new BasicDataModel(
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

  changeCurrentPage(page: number) {
    this.lastQuery.current_page = page;
    this.makeQuery(this.lastQuery, false);
  }

  changeSortBy(criteria: string) {
    this.lastQuery.sort_by = criteria;
    this.lastQuery.current_page = 1;
    this.makeQuery(this.lastQuery, true);
  }

  getLastQuery() {
    return this.lastQuery;
  }


}

