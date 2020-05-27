import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, Subject} from "rxjs";
import {BasicDataModel} from "../header/content/search-page/search-results/result/basic-data-model";
import {QueryModel} from "../header/content/search-page/search-form/query-model";
import {ActivatedRoute} from "@angular/router";
import {map} from "rxjs/operators";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable()
export class QueryService {

  basicDataPageSource = new Subject<BasicDataModel[]>();
  basicDataPage$ = this.basicDataPageSource.asObservable();

  resultCountSource = new Subject<number>();
  resultCount$ = this.resultCountSource.asObservable();


  constructor(private http: HttpClient, private activatedRoute: ActivatedRoute) {
  }


  makeQuery(queryData: QueryModel): void {

    this.http.post('api/query', queryData, httpOptions).subscribe(
      newPage => {
        let processedNewPage: BasicDataModel[] = QueryService.processPage(newPage);
        this.basicDataPageSource.next(processedNewPage);
      }
    );

    this.http.post('api/result_count', queryData, httpOptions).subscribe(newResultCount => {
      this.resultCountSource.next(<number>newResultCount);
    })

  }

  getMovieById(tid: number): Observable<BasicDataModel> {
    return this.http.post('api/movie_by_tid', {tid: tid}, httpOptions).pipe(map(page => QueryService.processPage(page)[0]));
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

