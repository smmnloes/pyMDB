import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, Subject} from "rxjs";
import {BasicDataModel} from "../components/content/search-page/search-results/result/basic-data-model";
import {QueryModel} from "../components/content/search-page/search-form/query-model";
import {ActivatedRoute} from "@angular/router";
import {map} from "rxjs/operators";
import {Util} from "../util/util";


@Injectable()
export class QueryService {

  basicDataPageSource = new Subject<BasicDataModel[]>();
  basicDataPage$ = this.basicDataPageSource.asObservable();

  resultCountSource = new Subject<number>();
  resultCount$ = this.resultCountSource.asObservable();


  constructor(private http: HttpClient, private activatedRoute: ActivatedRoute) {
  }


  makeQuery(queryData: QueryModel): void {

    this.http.post('api/movies/query', queryData, Util.appJsonHeaderOptions).subscribe(
      newPage => {
        let processedNewPage: BasicDataModel[] = QueryService.processPage(newPage);
        this.basicDataPageSource.next(processedNewPage);
      }
    );

    this.http.post('api/movies/result_count', queryData, Util.appJsonHeaderOptions).subscribe(newResultCount => {
      this.resultCountSource.next(<number>newResultCount);
    })

  }

  getMovieById(tid: number): Observable<BasicDataModel> {
    return this.http.post('api/movies/movie_by_tid', {tid: tid}, Util.appJsonHeaderOptions).pipe(map(page => QueryService.processPage(page)[0]));
  }


  static processPage(resultList: any): BasicDataModel[] {
    let results: BasicDataModel[] = [];
    for (let result of resultList) {
      results.push(new BasicDataModel(
        result['average_rating'],
        result['directors'],
        result['writers'],
        result['genres'],
        result['primary_title'],
        result['principals'],
        result['runtime_minutes'],
        result['tid'],
        result['year']
      ));

    }
    return results;
  }

}

