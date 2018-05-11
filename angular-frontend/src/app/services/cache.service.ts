import {Injectable} from '@angular/core';
import {BasicDataModel} from "../header/content/search-page/search-results/result/basic-data-model";
import {QueryModel} from "../header/content/search-page/search-form/query-model";

@Injectable()
export class CacheService {
  private cache: { [query: string]: { resultCount: number, pages: BasicDataModel[][] } } = {};


  constructor() {
  }


  public getResultCount(queryModel: QueryModel): number {
    return this.cache[queryModel.normalize()] == null ?
      null : this.cache[queryModel.normalize()].resultCount;
  }

  public getPage(queryModel: QueryModel): BasicDataModel[] {
    return this.cache[queryModel.normalize()] == null ?
      null : this.cache[queryModel.normalize()].pages[queryModel.current_page];
  }

  public setResultCount(queryModel: QueryModel, resultCount: number) {
    let normalized = queryModel.normalize();
    if (this.cache[normalized] == null) {
      this.cache[normalized] = {resultCount: resultCount, pages: []}
    } else {
      if (this.cache[normalized].resultCount == null) {
        this.cache[normalized].resultCount = resultCount;
      }
    }
  }

  public setPage(queryModel: QueryModel, page: BasicDataModel[]) {
    let normalized = queryModel.normalize();
    if (this.cache[normalized] == null) {
      this.cache[normalized] = {resultCount: null, pages: []};
    }
    this.cache[normalized].pages[queryModel.current_page] = page;
  }

}
