import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Subject} from "rxjs/Subject";
import {BasicDataModel} from "../header/content/search-page/search-results/result/basic-data-model";
import {QueryModel} from "../header/content/search-page/search-form/query-model";
import {Util} from "../util/util";
import {ActivatedRoute} from "@angular/router";
import {CacheService} from "./cache.service";


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

  constructor(private http: HttpClient, private activatedRoute: ActivatedRoute, private cacheService: CacheService) {
    this.activatedRoute.queryParams.subscribe(queryParams => {
      if (!Util.isEmpty(queryParams)) {
        this.makeQuery(QueryModel.fromQueryParams(queryParams));
      }
    });
  }


  makeQuery(queryData: QueryModel) {
    queryData.results_per_page = this.RESULTS_PER_PAGE;

    let cachedPage = this.cacheService.getPage(queryData);

    if (cachedPage != null) {
      console.log("CACHED PAGE");
      this.basicDataSource.next(cachedPage);
    } else {
      this.http.post('api/query', queryData, httpOptions).subscribe(
        newPage => {
          let processedNewPage: BasicDataModel[] = QueryService.processPage(newPage);
          this.basicDataSource.next(processedNewPage);

          this.cacheService.setPage(queryData, processedNewPage);
        }
      );
    }

    let cachedResultCount = this.cacheService.getResultCount(queryData);

    if (cachedResultCount != null) {
      console.log("CACHED RESULT COUNT");
      this.resultCountSource.next(cachedResultCount);

    } else {
      this.http.post('api/result_count', queryData, httpOptions).subscribe(newResultCount => {
        this.resultCountSource.next(<number>newResultCount);
        this.cacheService.setResultCount(queryData, <number>newResultCount);
      })
    }
  }


  static processPage(basicData): BasicDataModel[] {
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

