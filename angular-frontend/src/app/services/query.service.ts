import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Subject} from "rxjs";
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

  basicDataPageSource = new Subject<BasicDataModel[]>();
  basicDataPage$ = this.basicDataPageSource.asObservable();

  basicDataSingleSource = new Subject<BasicDataModel>();
  basicDataSingle$ = this.basicDataSingleSource.asObservable();

  resultCountSource = new Subject<number>();
  resultCount$ = this.resultCountSource.asObservable();


  constructor(private http: HttpClient, private activatedRoute: ActivatedRoute, private cacheService: CacheService) {
    this.activatedRoute.queryParams.subscribe(queryParams => {
      if (!Util.isEmpty(queryParams)) {
        this.makeQuery(QueryModel.fromQueryParams(queryParams));
      }
    });
  }


  makeQuery(queryData: QueryModel) {
    let cachedPage = this.cacheService.getPage(queryData);

    if (cachedPage != null) {

      //Timeout necessary, otherwise cached results won't be rendered if the user returns
      //to search page via the browser's back button
      setTimeout(() => {
        this.basicDataPageSource.next(cachedPage);
      }, 1);

    } else {
      this.http.post('api/query', queryData, httpOptions).subscribe(
        newPage => {
          let processedNewPage: BasicDataModel[] = QueryService.processPage(newPage);
          this.basicDataPageSource.next(processedNewPage);

          this.cacheService.setPage(queryData, processedNewPage);
        }
      );
    }

    let cachedResultCount = this.cacheService.getResultCount(queryData);

    if (cachedResultCount != null) {

      //See explanation above
      setTimeout(() => {
        this.resultCountSource.next(cachedResultCount);
      }, 1);

    } else {
      this.http.post('api/result_count', queryData, httpOptions).subscribe(newResultCount => {
        this.resultCountSource.next(<number>newResultCount);
        this.cacheService.setResultCount(queryData, <number>newResultCount);
      })
    }
  }

  getMovieById(tid: number) {
    this.http.post('api/movie_by_tid', {tid: tid}, httpOptions).subscribe(
      result => {
        let processedResult: BasicDataModel = QueryService.processPage(result)[0];
        this.basicDataSingleSource.next(processedResult);
      }
    );
  }


  static processPage(basicData): BasicDataModel[] {
    let results: BasicDataModel[] = [];
    for (let result of basicData) {
      results.push(new BasicDataModel(
        result.average_rating,
        result.directors,
        result.writers,
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

