import {Injectable} from '@angular/core';
import {BasicDataModel} from "../header/content/search-page/search-results/result/basic-data-model";
import {QueryModel} from "../header/content/search-page/search-form/query-model";
import {DetailedDataModel} from "../header/content/search-page/search-results/result/detailed-data-model";

@Injectable()
export class CacheService {
  private cache_BasicData: { [query: string]: { resultCount: number, pages: BasicDataModel[][] } } = {};
  private cache_DetailedData: { [IMDB_id: number]: DetailedDataModel } = {};


  constructor() {
  }


  public getResultCount(queryModel: QueryModel): number {
    let normalized = queryModel.normalize();
    return this.cache_BasicData[normalized] == null ?
      null : this.cache_BasicData[normalized].resultCount;
  }

  public getPage(queryModel: QueryModel): BasicDataModel[] {
    let normalized = queryModel.normalize();
    return this.cache_BasicData[normalized] == null ?
      null : this.cache_BasicData[normalized].pages[queryModel.current_page];
  }

  public setResultCount(queryModel: QueryModel, resultCount: number) {
    let normalized = queryModel.normalize();
    if (this.cache_BasicData[normalized] == null) {
      this.cache_BasicData[normalized] = {resultCount: resultCount, pages: []}
    } else {
      if (this.cache_BasicData[normalized].resultCount == null) {
        this.cache_BasicData[normalized].resultCount = resultCount;
      }
    }
  }

  public setPage(queryModel: QueryModel, page: BasicDataModel[]) {
    let normalized = queryModel.normalize();
    if (this.cache_BasicData[normalized] == null) {
      this.cache_BasicData[normalized] = {resultCount: null, pages: []};
    }
    this.cache_BasicData[normalized].pages[queryModel.current_page] = page;
  }

  public setDetails(IMDB_Id: number, details: DetailedDataModel) {
    this.cache_DetailedData[IMDB_Id] = details;
  }

  public getDetails(IMDB_Id: number) {
    return this.cache_DetailedData[IMDB_Id];

  }
}
