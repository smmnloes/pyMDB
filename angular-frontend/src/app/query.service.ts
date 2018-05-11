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

  RESULTS_PER_PAGE = 15;

  constructor(private http: HttpClient) {
  }


  makeQuery(queryData: QueryModel) {
    this.getResultCount(queryData);

    queryData.results_per_page = this.RESULTS_PER_PAGE;

    this.http.post('api/query', queryData, httpOptions).subscribe(
      data => {
        let processedResult: BasicDataModel[] = QueryService.processBasicData(data);
        this.basicDataSource.next(processedResult);
      }
    );

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

}

